# Review - last check before handing work over

Run on deliverables only (a UI, a document, a campaign, a feature). Skip for quick answers.

## 1. Brief check

- Does it do what the user asked, and nothing big they did not ask for?
- Does it respect `.claude/CONTEXT.md` preferences and `DESIGN.md`?

## 2. Correctness

- Code: builds, tests/lint pass if the project has them, no leftover debug output.
- Web UI: no console errors or failed requests; renders at all breakpoints (`build/browser-checks.md`, when the browser plugin is installed).
- Facts and numbers: each one traceable to a source or the user.
- Links and paths: valid.

## 3. AI-tell audit

Launch the `critic` agent with the relevant list:
- UI -> `build/design/craft-floor.md`
- Security-sensitive change -> a quick `build/security-audit.md` guidance pass on the diff
- Code -> `build/deslop-code.md` table
- Images and thumbnails -> `build/deslop-media.md` list
- Video -> `build/video/tells.md`, plus `scripts/video_check.py` on the render
- Prose -> `write/humanize-text.md` patterns

Fix what it finds. Do not present the critic's raw report unless the user asks.

## 4. Report honestly

Say what was done, what was verified, and what was not (for example "not tested on mobile"). One short paragraph.
