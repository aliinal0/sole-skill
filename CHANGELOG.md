# Changelog

## 1.1.0 - 2026-11-21 - five skills, lazy-senior coding

Sole is now five skills that share one module library: `sole:code`, `sole:visual`, `sole:write`, `sole:business` and the general `sole:sole`. Each skill has its own description, so each area gets precise trigger words. A request loads only its own area's table: 433 to 555 words instead of the 822-word router, or 877 for `sole:code`, which carries its coding rules inline.

Test results: 38 of 41 eval cases pass with Sole, 18 of 41 without. Cost per passing answer is $0.19 with Sole and $0.28 without (API list prices).

- **`sole:code`**: works like a lazy senior developer.
  - Before writing, it checks what the codebase, the standard library or an installed package already does. It adds no options, layers or dependencies nobody asked for.
  - It leaves a small test or self-check for logic that can break and marks deliberate shortcuts with `shortcut:` comments.
  - It ends its reply with what it did not check.
- **`/sole:review`**: reviews a change or the whole repo. Findings are ranked by correctness, safety, load, tests, speed and lean code, and each one needs a concrete failing case. `shortcuts` lists the deferred work.
- **Shared rules**:
  - Every skill carries the same block: limits, facts, economy, finish.
  - CI and `evals/run.py` fail if any copy differs.
  - New economy rules for large models and high effort: stop exploring once you can act; read files in one batch; use subagents only for wide work; use the critic agent only for large deliverables or on request.
- **Hooks**:
  - The after-skill hook now prints the library's absolute path, so module paths resolve from any of the five skills.
  - The session hint is shorter.
- **Tests**:
  - New cases `code-lean` and `code-review`.
  - The runner checks every skill's description size and name.
- Known trade-off: the five descriptions add about 2,200 characters to every session's always-loaded text.

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
