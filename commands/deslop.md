---
description: Remove AI tells from a UI, code, media plan or text
argument-hint: "[path, URL or pasted text]"
---
Invoke the Skill `sole:sole` first (its result gives the skill's base directory); module paths below are relative to it. Target: $ARGUMENTS (if empty, use the current project's UI or the last deliverable).

Detect the type and load the matching module: UI -> `build/deslop-ui.md`, code -> `build/deslop-code.md`, video -> `build/video/tells.md`, images and generator prompts -> `build/deslop-media.md`, prose -> `write/humanize-text.md`. Run the `critic` agent first, show the top findings in a short list, then fix them. Keep every fact and every behaviour unchanged.
