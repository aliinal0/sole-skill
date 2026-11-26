---
disable-model-invocation: true
description: Create, update or show the project memory file (.sole/CONTEXT.md)
argument-hint: "[show | save <note> | handoff]"
---
Invoke the Skill `sole:sole` first (the hook after it prints the Sole library path), then read from the library and follow `core/context-memory.md`.

Argument: $ARGUMENTS
- empty or `save <note>`: update `.sole/CONTEXT.md` with the decisions, preferences, progress and next steps from this session (plus the note, if given). If the file does not exist, ask once before creating it from `templates/CONTEXT.md`. Use the `memory-keeper` agent.
- `show`: print the current file, nothing else.
- `handoff`: refresh the file for a fresh session and add a `## Suggested start` line.
