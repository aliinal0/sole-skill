#!/usr/bin/env python3
"""Fetch a public URL as readable text using a fallback chain.

Order: direct HTTP -> Jina Reader (r.jina.ai) -> Firecrawl (only if FIRECRAWL_API_KEY is set).
Prints the content to stdout and the method used to stderr. Standard library only.

This script does not solve CAPTCHAs, log in, or bypass paywalls or bot protection.
"""
import argparse
import html
import http.client
import ipaddress
import json
import os
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Certificate checks stay ON. The system trust store is used, plus the certifi
# bundle when it is installed (fixes "unable to get local issuer certificate"
# on Windows Python, which cannot fetch missing root certificates on demand).
SSL_CTX = ssl.create_default_context()
try:
    import certifi

    SSL_CTX.load_verify_locations(certifi.where())
except (ImportError, OSError):
    pass

UA = "Mozilla/5.0 (compatible; sole-skill-fetch/1.0)"
TIMEOUT = 30
# A bot check (CAPTCHA or challenge page) stops the whole chain: routing the page through
# another service to get past it would be evading the site's bot protection.
BOT_CHECK_MARKERS = (
    "just a moment...",
    "attention required",
    "checking your browser",
    "verify you are human",
    "verifying you are human",
    "confirm you are a human",
    "are you a robot",
    "complete the captcha",
    "access denied",
    "unusual traffic",
    "pardon our interruption",
    "press & hold",
    "please complete the security check",
)
# A page that is empty or needs JavaScript may be read by a renderer (Jina, Firecrawl).
BLOCK_MARKERS = (
    "enable javascript",
)
# The site refused us (login needed, forbidden, rate limited): asking another service to fetch it would get around that.
REFUSED_STATUS = {401, 403, 429}
# The page does not exist: a reader cannot find it either, and asking one would only share the URL.
MISSING_STATUS = {404, 410}
HTML_RE = re.compile(r"<(?:!doctype|html|head|body|p|div|h[1-6]|main|article|pre|table|ul)[\s>/]", re.I)
MAX_BYTES = 5_000_000


class BotCheck(RuntimeError):
    """The page answered with a CAPTCHA, a bot-check challenge or an access refusal."""


class Missing(RuntimeError):
    """The page does not exist (404 or 410)."""


def unsafe_target(url):
    """Why this URL must not be fetched, or None. Stops a prompt-injected page from pointing the script at the
    user's own machine or network, and keeps credentials in a URL away from third-party readers."""
    parts = urllib.parse.urlsplit(url)
    if parts.username or parts.password:
        return "the URL contains a username or password"
    try:
        infos = socket.getaddrinfo(parts.hostname or "", None)
    except (OSError, UnicodeError):
        return None  # does not resolve here; the fetch itself will fail or a public reader will
    for info in infos:
        ip = ipaddress.ip_address(info[4][0].split("%")[0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            return f"{parts.hostname} is a local or private address ({ip})"
    return None


class _CheckedRedirect(urllib.request.HTTPRedirectHandler):
    """A public page must not redirect the script to a local or private address."""
    allow_private = False

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        why = None if self.allow_private else unsafe_target(newurl)
        if why:
            raise urllib.error.URLError(f"redirect refused: {why}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _get(url, headers=None, data=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=SSL_CTX), _CheckedRedirect)
    with opener.open(req, timeout=TIMEOUT) as r:
        return r.status, r.read(MAX_BYTES).decode(r.headers.get_content_charset() or "utf-8", "replace")


def html_to_text(raw):
    for tag in ("main", "article"):
        m = re.search(rf"(?is)<{tag}\b[^>]*>(.*)</{tag}>", raw)
        if m and len(m.group(1)) > 500:
            raw = m.group(1)
            break
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr)>", "\n", raw)
    raw = re.sub(r"(?s)<[A-Za-z/!][^>]*>", " ", raw)   # a bare "<" in text (a < b) is not a tag
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t]+", " ", raw)
    return re.sub(r"\n\s*\n+", "\n\n", raw).strip()


def is_bot_check(raw):
    """A short page whose visible text is a challenge. Scripts are ignored: many normal pages load
    a CAPTCHA widget for a form, and a long article may mention CAPTCHAs without being one."""
    text = html_to_text(raw) if "<" in raw[:2000] else raw
    low = text[:3000].lower()
    return len(text) < 2000 and any(m in low for m in BOT_CHECK_MARKERS)


def looks_blocked(text):
    low = text[:3000].lower()
    return len(text.strip()) < 150 or any(m in low for m in BLOCK_MARKERS)


def direct(url):
    try:
        status, body = _get(url)
    except urllib.error.HTTPError as e:   # a 503 page can still be a challenge
        if e.code in REFUSED_STATUS:
            raise BotCheck(f"the site refused the request (status {e.code})") from e
        if e.code in MISSING_STATUS:
            raise Missing(f"the page does not exist (status {e.code})") from e
        body = e.read(MAX_BYTES).decode("utf-8", "replace")
        if is_bot_check(body):
            raise BotCheck(f"direct fetch got a bot check (status {e.code})") from e
        raise
    if is_bot_check(body):
        raise BotCheck(f"direct fetch got a bot check (status {status})")
    text = html_to_text(body) if HTML_RE.search(body[:2000]) else body
    if status >= 400 or looks_blocked(text):
        raise RuntimeError(f"direct fetch looks blocked (status {status})")
    return text


def jina(url):
    headers = {"Accept": "text/plain"}
    key = os.environ.get("JINA_API_KEY")
    if key:
        headers["Authorization"] = f"Bearer {key}"
    last = None
    for attempt in range(3):
        try:
            _, body = _get("https://r.jina.ai/" + url, headers=headers)
            if is_bot_check(body):
                raise BotCheck("jina got a bot check")
            if "upstream connect error" in body or looks_blocked(body):
                raise RuntimeError("jina returned an error or blocked page")
            return body
        except BotCheck:
            raise
        except Exception as e:  # noqa: BLE001 - retry any transient failure
            last = e
            time.sleep(1 + attempt)
    raise RuntimeError(f"jina failed: {last}")


def firecrawl(url):
    key = os.environ.get("FIRECRAWL_API_KEY")
    if not key:
        raise RuntimeError("FIRECRAWL_API_KEY not set")
    payload = json.dumps({"url": url, "formats": ["markdown"]}).encode()
    _, body = _get(
        "https://api.firecrawl.dev/v1/scrape",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        data=payload,
    )
    md = (json.loads(body).get("data") or {}).get("markdown") or ""
    if is_bot_check(md):
        raise BotCheck("firecrawl got a bot check")
    if looks_blocked(md):
        raise RuntimeError("firecrawl returned little or blocked content")
    return md


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("url")
    p.add_argument("--max-chars", type=int, default=20000, help="truncate output (0 = no limit)")
    p.add_argument("--skip-direct", action="store_true", help="start with Jina Reader")
    p.add_argument("--allow-private", action="store_true",
                   help="the user asked for a page on their own machine or network: fetch it directly only")
    a = p.parse_args()

    if not re.match(r"^https?://", a.url):
        sys.exit("error: URL must start with http:// or https://")
    why = unsafe_target(a.url)
    if why and not a.allow_private:
        sys.exit(f"error: not fetching: {why}. If the user asked for this page, rerun with --allow-private "
                 "(direct fetch only, never through a third-party reader).")

    _CheckedRedirect.allow_private = a.allow_private
    chain = [] if why else [("jina", jina), ("firecrawl", firecrawl)]
    if not a.skip_direct or why:
        chain.insert(0, ("direct", direct))

    errors = []
    for name, fn in chain:
        try:
            text = fn(a.url)
            for err in errors:
                print(f"[fetch.py] skipped {err}", file=sys.stderr)
            print(f"[fetch.py] method={name} chars={len(text)}", file=sys.stderr)
            if a.max_chars and len(text) > a.max_chars:
                text = text[: a.max_chars] + f"\n\n[truncated at {a.max_chars} chars]"
            sys.stdout.reconfigure(encoding="utf-8")
            print(text)
            return
        except BotCheck as e:
            print(f"[fetch.py] stopped: {e}. This script does not route around CAPTCHAs, bot checks or access refusals.",
                  file=sys.stderr)
            print("Ask the user to open the page in their own browser and paste or export the content, "
                  "or use the site's official API.", file=sys.stderr)
            sys.exit(3)
        except Missing as e:
            print(f"[fetch.py] stopped: {e}. Check the address with the user.", file=sys.stderr)
            sys.exit(1)
        # OSError covers URLError, timeouts, resets, SSL errors and RemoteDisconnected;
        # HTTPException covers IncompleteRead and other protocol errors.
        except (OSError, http.client.HTTPException, RuntimeError, ValueError, LookupError) as e:
            errors.append(f"{name}: {e}")

    print("[fetch.py] all methods failed:\n  " + "\n  ".join(errors), file=sys.stderr)
    print("Ask the user to paste the page content, or try a browser tool.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
