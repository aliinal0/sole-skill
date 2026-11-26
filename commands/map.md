---
disable-model-invocation: true
description: Build or refresh a code map so future sessions understand the repo without re-reading it
argument-hint: "[graphify | lite | update]"
---
Invoke the Skill `sole:code` first (the hook after it prints the Sole library path), then read from the library and follow `build/code-map.md`. Option: $ARGUMENTS

- `graphify`: use the graphify tool (ask before installing it).
- `lite` or empty: build `.sole/CODEMAP.md` with parallel explore agents.
- `update`: refresh the existing map for recent changes.
Add the map's path to `.sole/CONTEXT.md` -> Key files.
