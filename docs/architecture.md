# Architecture

## Five skills, one library

Claude Code puts the name and description of every installed skill into context at session start, and picks skills by matching those descriptions. Many skills with overlapping triggers ("design", "copy", "research") cost tokens on every session and fire inconsistently.

Sole has five skills with areas that do not overlap, and one shared library of modules:

| Skill | Area | Body loaded on trigger |
|---|---|---|
| `sole:code` | Writing, fixing, refactoring and reviewing code; security review; code maps; browser checks | The lazy-senior coding rules, so most coding needs no module read |
| `sole:visual` | UI and design, images and generator prompts, video editing and motion graphics | Routing table |
| `sole:write` | Any text: docs, READMEs, UI text, emails, posts; humanizing; the user's voice | Routing table |
| `sole:business` | Ads, ideas, competitors, SEO and GEO, positioning and pricing, conversion | Routing table |
| `sole:sole` | Research, blocked pages, teaching, specialist personas, project memory, setup fixes, final checks | Routing table, file conventions; it also holds the library |

Each skill has its own description (up to 1,024 characters), so each area gets precise trigger words, and a request loads one small table instead of a table for everything.

## Three loading levels

1. **Always loaded**: the descriptions of the five skills and six agents (commands are user-invoked only, so theirs are not loaded), and a one-line hint from the SessionStart hook.
2. **On trigger**: the body of one `SKILL.md`: its table and the Shared rules block. A PostToolUse hook then prints the library's absolute path and reminds Claude to read the routed module.
3. **On demand**: one or two module files from the library (`skills/sole/`: `core/`, `build/`, `business/`, `research/`, `write/`), plus templates and scripts only when a module asks for them.

## Shared rules

Every `SKILL.md` carries the same "Shared rules" block: library location, memory, intent, facts, economy, finish, agents and hard limits. `evals/run.py` and CI fail if one copy differs from `skills/sole/SKILL.md`, so the limits cannot drift apart between skills. Edit the block in `skills/sole/SKILL.md` and copy it to the other four.

## Layers

```
 sole:code   sole:visual   sole:write   sole:business   sole:sole
     \            |             |              |            /
      └──── library: skills/sole/ (core, build, business, research, write) ────┘
                                   |
                       shared agents (agents/)
   researcher · web-fetcher · critic · strategist · memory-keeper · security-auditor
```

- **Modules are independent**: each can be read alone. They reference each other by library path when combined (e.g. `business/ads.md` -> `write/humanize-text.md`), whichever skill loaded them.
- **Agents are shared**: no module defines its own subagent; a few use Claude Code's built-in Explore or general-purpose agents. This keeps behaviour consistent and lets modules run work in parallel.

## Persistence

Notes live in `.sole/` rather than `.claude/`, because Claude Code asks before every write under `.claude/`.

| File | Owner | Purpose |
|---|---|---|
| `.sole/CONTEXT.md` | `core/context-memory.md`, `memory-keeper` | Goal, preferences, decisions, progress, next steps, reminders |
| `.sole/CODEMAP.md` | `build/code-map.md` | Lightweight map of the codebase |
| `.sole/VOICE.md` | `write/humanize-text.md` | The user's writing voice profile |
| `.sole/EDITSTYLE.md` | `build/video/edit.md` | The user's editing style |
| `.sole/research/`, `.sole/competitors/`, `.sole/seo-baseline/` | research, competitor and SEO modules | Caches: source lists, raw competitor notes |
| `DESIGN.md`, `PRODUCT.md` | `build/deslop-ui.md`, `build/design/commands.md` | Design system and product context (shared with other design tools) |
| `docs/sole/<type>/*.md` | research, competitor, security modules | Reports for people (asked once before the first write) |

The SessionStart hook (`hooks/load-context.sh`) prints the one-line hint and `.sole/CONTEXT.md` (first 200 lines; it falls back to `.claude/CONTEXT.md`, where versions before 1.2.0 kept it) at startup, resume, clear and after compaction. The file is framed as notes, not commands, so a CONTEXT.md planted in a cloned repo cannot order Claude around.
