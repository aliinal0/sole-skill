# Changelog

## 1.0.0 - 2026-11-21 - first public release

One adaptive Claude Code skill in place of many overlapping ones. A router (`SKILL.md`) loads only the module a request needs.

Test results: 34 of 39 eval cases pass with Sole, 17 of 39 without. Sole costs about 1.4x a plain answer overall, but $0.20 per passing answer against $0.29 without (API list prices).

### What is in it

- **Modules**:
  - Build: UI design, video editing and motion graphics, code, images, security review, browser checks, code map, final review.
  - Business: ads, ideas, competitors, SEO and GEO, pricing, conversion.
  - Research: web access, deep research, learning.
  - Write: humanizing text, the user's voice, docs and copy.
  - Core: intent, token economy, project memory, retrospectives.
- **Router rules**: Sole reads the routed module before answering, and states as fact only what the user gave or it checked.
- **Commands**: 15 slash commands, including `/sole:video` to plan, edit or review a video and to learn a creator's editing style.
- **Agents**: six shared agents, plus about 50 specialist personas fetched on demand.
- **Hooks**:
  - A SessionStart hook loads the project memory file.
  - A hook that runs after the skill loads reminds Claude to read the module first.
- **Scripts**:
  - `fetch.py` reads pages that fail to load directly. It stops at any CAPTCHA or bot check.
  - `video_check.py` measures shot rhythm, pauses and loudness, with thresholds taken from 40 human-edited films.
- **Optional `sole-browser` plugin**: Chrome DevTools MCP, headless, with an isolated profile.
- **Tests**:
  - 39 eval cases, at least one for every module.
  - 18 unit tests for the scripts.
  - `evals/run.py` runs all of it with one command. It starts with free checks and caches results, so only changed cases cost tokens.

### Known limits

Tested on Claude Code 2.1 on Windows only. Rules and examples are written for English text.

### Sources

Sole condenses and rewrites ideas from more than 20 open-source skills and tools; see `CREDITS.md`. video-editor-skills was reviewed but not used, because its licence (CC BY-NC 4.0) does not allow commercial use.
