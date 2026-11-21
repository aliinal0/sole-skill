---
description: Remove AI tells from a UI, code, media plan or text
argument-hint: "[path, URL or pasted text]"
---
Invoke the Sole skill for the target's type first (`sole:visual` for UI, images or video, `sole:code` for code, `sole:write` for text); the hook after it prints the Sole library path, and module paths below are relative to it. Target: $ARGUMENTS (if empty, use the current project's UI or the last deliverable).

Detect the type and load the matching module: UI -> `build/deslop-ui.md`, code -> `build/deslop-code.md`, video -> `build/video/tells.md`, images and generator prompts -> `build/deslop-media.md`, prose -> `write/humanize-text.md`. Audit it against that list (the `critic` agent for a large target), show the top findings in a short list, then fix them. Keep every fact and every behaviour unchanged.
