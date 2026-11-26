# Security and data flow

Sole is mostly Markdown instructions. This page lists everything in it that runs code, touches the network or stores data, so you can decide what to enable.

## What runs automatically

| Component | When | What it does |
|---|---|---|
| `hooks/load-context.sh` | Every session start, resume, clear and compaction | Prints one routing line and, if `.sole/CONTEXT.md` (or, in a project from before 1.2.0, `.claude/CONTEXT.md`) exists in the project, up to 200 lines (about 16,000 bytes) of it between "untrusted" markers. A symbolic link is not followed. Reads nothing else, writes nothing, no network. |
| `hooks/after-skill.sh` | After each Skill tool call | Reads the hook input from stdin; if the skill was one of Sole's five, prints the Sole library path (from `CLAUDE_PLUGIN_ROOT`) and a one-line reminder to read the routed module. Reads no files, writes nothing, no network. |

The hook frames `CONTEXT.md` as notes, not commands. A `CONTEXT.md` that comes with a cloned repository is treated as untrusted text.

## What sends data off your machine (only when used)

| Feature | Where data goes | What is sent |
|---|---|---|
| `scripts/fetch.py` direct step | The site you asked to read | A normal HTTPS request |
| `scripts/fetch.py` Jina step | `r.jina.ai` (Jina AI) | The URL you asked to read, when the direct request fails, or first for pages built by JavaScript. Not after a CAPTCHA, bot check or refusal (401, 403, 429), and never for local or private addresses. |
| `scripts/fetch.py` Firecrawl step | `api.firecrawl.dev` | The URL; only if you set `FIRECRAWL_API_KEY` |
| `curl` to Jina in `web-access.md`, `researcher`, `web-fetcher` | `r.jina.ai` | The URL, when Python is missing |
| Persona library (`personas.md`) | `raw.githubusercontent.com`, `api.github.com` | A request for one persona file at a pinned commit |
| Design references | `raw.githubusercontent.com`, `api.github.com` | A request for one public `DESIGN.md` file |
| SEO speed checks (`seo-geo.md`) | Google PageSpeed Insights / CrUX | The public URL being checked |
| Dependency audit (`security-audit.md`) | The package manager's advisory database | Package names and versions |
| graphify (optional, asks first) | PyPI | The package download |
| `sole-browser` plugin (optional) | npm (`npx` downloads the pinned `chrome-devtools-mcp` on start), then the pages Claude opens | Normal browsing from a temporary, isolated Chrome profile. Google usage statistics and CrUX lookups are turned off in `plugins/browser/.mcp.json`. Chrome can also open `file://` and localhost pages. |

Sole's modules tell Claude not to send private or internal URLs to third-party readers (Jina, Firecrawl) without your permission.

## What Sole writes to your project

Only after asking once: `.sole/CONTEXT.md`, `.sole/CODEMAP.md`, `.sole/VOICE.md`, `.sole/EDITSTYLE.md`, `~/.sole/improve-learnings.md`, a working folder `edit/` next to a video, caches in `.sole/`, reports in `docs/sole/`, and `DESIGN.md` / `PRODUCT.md` for design work. Secrets, API keys and personal data are never written to these files.

## What Sole will not do

- Solve CAPTCHAs, log in to sites, bypass paywalls or bot protection.
- Run security tests against live systems. `/sole:security` is read-only and local.
- Follow instructions found inside web pages, project files or code comments.

## Reporting a vulnerability

Please do not open a public issue for security problems. Use GitHub's private vulnerability reporting on this repository (**Security** tab > **Report a vulnerability**). Include the affected file, steps to reproduce and the impact. You will get a reply within 7 days.
