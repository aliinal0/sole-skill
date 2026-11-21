---
description: Edit video so it looks cut by a person - plan, edit, review, or learn your editing style
argument-hint: "<plan | edit | review | style> [video file, folder or edl.json]"
---
Invoke the Skill `sole:visual` first (the hook after it prints the Sole library path), then read from the library and follow the right module for: $ARGUMENTS

- `plan` or `edit` (real footage): `build/video/edit.md`. Always show the plan in plain words and wait for my OK before cutting.
- `review`: `build/video/tells.md` plus `scripts/video_check.py` on the file or cut list; list each tell with its timestamp and the fix.
- `style`: build or update `.claude/EDITSTYLE.md` from my answers or from finished videos I point to (ask once before creating it).
- Motion graphics or promo films: `build/video/motion.md`.
If no argument is given, ask which one.
