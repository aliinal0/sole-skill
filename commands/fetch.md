---
description: Read a URL the normal fetch cannot open (Jina / Firecrawl fallback)
argument-hint: "<url> [what to extract]"
---
Invoke the Skill `sole:sole` first (its result gives the skill's base directory), then read from that directory and follow `research/web-access.md` for: $ARGUMENTS

Return a short summary or the requested fields, and say which method worked. Never bypass logins, paywalls or CAPTCHAs.
