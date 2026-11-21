#!/usr/bin/env python3
"""Fetch a public URL as readable text using a fallback chain.

Order: direct HTTP -> Jina Reader (r.jina.ai) -> Firecrawl (only if FIRECRAWL_API_KEY is set).
Prints the content to stdout and the method used to stderr. Standard library only.

This script does not solve CAPTCHAs, log in, or bypass paywalls or bot protection.
"""
import argparse
import html
import http.client
import json
import os
import re
import ssl
import sys
import time
import urllib.error
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
)
# A page that is empty or needs JavaScript may be read by a renderer (Jina, Firecrawl).
BLOCK_MARKERS = (
    "enable javascript",
    "access denied",
)


class BotCheck(RuntimeError):
    """The page answered with a CAPTCHA or bot-check challenge."""


def _get(url, headers=None, data=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CTX) as r:
        return r.status, r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")


def html_to_text(raw):
    for tag in ("main", "article"):
        m = re.search(rf"(?is)<{tag}\b[^>]*>(.*)</{tag}>", raw)
        if m and len(m.group(1)) > 500:
            raw = m.group(1)
            break
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr)>", "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
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
    except urllib.error.HTTPError as e:   # 403/429/503 pages can still be a challenge
        body = e.read().decode("utf-8", "replace")
        if is_bot_check(body):
            raise BotCheck(f"direct fetch got a bot check (status {e.code})") from e
        raise
    if is_bot_check(body):
        raise BotCheck(f"direct fetch got a bot check (status {status})")
    text = html_to_text(body) if "<html" in body[:2000].lower() else body
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
    a = p.parse_args()

    if not re.match(r"^https?://", a.url):
        sys.exit("error: URL must start with http:// or https://")

    chain = [("jina", jina), ("firecrawl", firecrawl)]
    if not a.skip_direct:
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
            print(f"[fetch.py] stopped: {e}. This script does not route around CAPTCHAs or bot checks.",
                  file=sys.stderr)
            print("Ask the user to open the page in their own browser and paste or export the content, "
                  "or use the site's official API.", file=sys.stderr)
            sys.exit(3)
        # OSError covers URLError, timeouts, resets, SSL errors and RemoteDisconnected;
        # HTTPException covers IncompleteRead and other protocol errors.
        except (OSError, http.client.HTTPException, RuntimeError, ValueError) as e:
            errors.append(f"{name}: {e}")

    print("[fetch.py] all methods failed:\n  " + "\n  ".join(errors), file=sys.stderr)
    print("Ask the user to paste the page content, or try a browser tool.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
