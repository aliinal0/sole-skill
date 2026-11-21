---
description: Create, update or show the project memory file (.claude/CONTEXT.md)
argument-hint: "[show | save <note> | handoff]"
---
Invoke the Skill `sole:sole` first (its result gives the skill's base directory), then read from that directory and follow `core/context-memory.md`.

Argument: $ARGUMENTS
- empty or `save <note>`: update `.claude/CONTEXT.md` with the decisions, preferences, progress and next steps from this session (plus the note, if given). If the file does not exist, ask once before creating it from `templates/CONTEXT.md`. Use the `memory-keeper` agent.
- `show`: print the current file, nothing else.
- `handoff`: refresh the file for a fresh session and add a `## Suggested start` line.
