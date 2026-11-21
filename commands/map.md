---
description: Build or refresh a code map so future sessions understand the repo without re-reading it
argument-hint: "[graphify | lite | update]"
---
Invoke the Skill `sole:sole` first (its result gives the skill's base directory), then read from that directory and follow `build/code-map.md`. Option: $ARGUMENTS

- `graphify`: use the graphify tool (ask before installing it).
- `lite` or empty: build `.claude/CODEMAP.md` with parallel explore agents.
- `update`: refresh the existing map for recent changes.
Add the map's path to `.claude/CONTEXT.md` -> Key files.
