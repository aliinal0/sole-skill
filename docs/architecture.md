# Architecture

## Why one router instead of many skills

Claude Code puts the name and description of every installed skill into context at session start, and picks skills by matching those descriptions. Ten skills with overlapping triggers ("design", "copy", "research") cost tokens on every session and fire inconsistently. Sole exposes one description and decides internally.

## Three loading levels

1. **Always loaded**: the `description` in `skills/sole/SKILL.md` frontmatter (~150 words).
2. **On trigger**: the body of `SKILL.md` - the routing table and core rules (~60 lines). A PostToolUse hook then reminds Claude to read the routed module.
3. **On demand**: one or two module files from `core/`, `build/`, `business/`, `research/`, `write/`, plus templates and scripts only when a module asks for them.

## Layers

```
            ┌──────────── SKILL.md (router) ────────────┐
            │  Route + read module -> core rules        │
            └───────┬──────────┬───────────┬────────┬───┘
                 build/    business/   research/  write/
                    \          |          |        /
                     └── shared agents (agents/) ─┘
   researcher · web-fetcher · critic · strategist · memory-keeper · security-auditor
```

- **Core** is not a category; it runs for every request.
- **Modules are independent**: each can be read alone. They reference each other by path when combined (e.g. `business/ads.md` -> `write/humanize-text.md`).
- **Agents are shared**: no module defines its own subagent. This keeps behaviour consistent and lets modules run work in parallel.

## Persistence

| File | Owner | Purpose |
|---|---|---|
| `.claude/CONTEXT.md` | `core/context-memory.md`, `memory-keeper` | Goal, preferences, decisions, progress, next steps, reminders |
| `.claude/CODEMAP.md` | `build/code-map.md` | Lightweight map of the codebase |
| `.claude/VOICE.md` | `write/humanize-text.md` | The user's writing voice profile |
| `.claude/sole/` | research and competitor modules | Caches: source lists, raw competitor notes |
| `DESIGN.md`, `PRODUCT.md` | `build/deslop-ui.md`, `build/design/commands.md` | Design system and product context (shared with other design tools) |
| `docs/sole/<type>/*.md` | research, competitor, security modules | Reports for people (asked once before the first write) |

The SessionStart hook (`hooks/load-context.sh`) prints a one-line routing hint and `.claude/CONTEXT.md` (first 200 lines) at startup, resume, clear and after compaction. The file is framed as notes, not commands, so a CONTEXT.md planted in a cloned repo cannot order Claude around.
