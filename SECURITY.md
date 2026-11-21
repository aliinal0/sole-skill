# Security and data flow

Sole is mostly Markdown instructions. This page lists everything in it that runs code, touches the network or stores data, so you can decide what to enable.

## What runs automatically

| Component | When | What it does |
|---|---|---|
| `hooks/load-context.sh` | Every session start, resume, clear and compaction | Prints one routing line and, if `.claude/CONTEXT.md` exists in the project, its first 200 lines. Reads nothing else, writes nothing, no network. |
| `hooks/after-skill.sh` | After each Skill tool call | Reads the hook input from stdin; if the skill was Sole, prints a one-line reminder to read the routed module. Reads no files, writes nothing, no network. |

The hook frames `CONTEXT.md` as notes, not commands. A `CONTEXT.md` that comes with a cloned repository is treated as untrusted text.

## What sends data off your machine (only when used)

| Feature | Where data goes | What is sent |
|---|---|---|
| `scripts/fetch.py` direct step | The site you asked to read | A normal HTTPS request |
| `scripts/fetch.py` Jina step | `r.jina.ai` (Jina AI) | The URL you asked to read. Used only when the direct request fails or looks blocked. |
| `scripts/fetch.py` Firecrawl step | `api.firecrawl.dev` | The URL; only if you set `FIRECRAWL_API_KEY` |
| Persona library (`personas.md`) | `raw.githubusercontent.com` | A request for one persona file at a pinned commit |
| Design references | `raw.githubusercontent.com` | A request for one public `DESIGN.md` file |
| `sole-browser` plugin (optional) | The pages Claude opens | Normal browsing from a temporary, isolated Chrome profile. Google usage statistics and CrUX lookups are turned off in `plugins/browser/.mcp.json`. |

Sole's modules tell Claude not to send private or internal URLs to third-party readers (Jina, Firecrawl) without your permission.

## What Sole writes to your project

Only after asking once: `.claude/CONTEXT.md`, `.claude/CODEMAP.md`, `.claude/VOICE.md`, caches in `.claude/sole/`, reports in `docs/sole/`, and `DESIGN.md` / `PRODUCT.md` for design work. Secrets, API keys and personal data are never written to these files.

## What Sole will not do

- Solve CAPTCHAs, log in to sites, bypass paywalls or bot protection.
- Run security tests against live systems. `/sole:security` is read-only and local.
- Follow instructions found inside web pages, project files or code comments.

## Reporting a vulnerability

Please do not open a public issue for security problems. Use GitHub's private vulnerability reporting on this repository (**Security** tab > **Report a vulnerability**). Include the affected file, steps to reproduce and the impact. You will get a reply within 7 days.
