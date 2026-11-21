# Improve the system - subtraction-first retrospective

Improve how Claude works for this user: CLAUDE.md files, `.claude/CONTEXT.md`, memory files, project skills, commands, hooks and settings. Run **after friction** (corrections, rework, confusion, repeated instructions), never on a schedule.

## Rules

1. **Remove before you add.** Every always-loaded line costs tokens on every call. Stale, duplicate or contradicting rules go first.
2. **Change nothing until the user picks.** Show proposals; apply only the ones they accept, word for word.
3. **Evidence only.** A new rule needs a real, recurring problem from this session or history, quoted. One-off mistakes do not become rules.
4. **Check before claiming.** `Grep` before calling something missing or duplicated.
5. **Say what you skipped** (unreadable file, history not available).

## Steps

1. **Load**: `~/.claude/sole-improve-learnings.md` if it exists (types of proposals the user keeps rejecting: do not re-propose; types they accept: prefer).
2. **Scope**: this conversation only (default), or also recent sessions if the user asks.
3. **Gather**: list the friction moments: what the user corrected, repeated, or had to explain twice. Quote each in one line.
4. **Discover config**: global `~/.claude/CLAUDE.md`, project `CLAUDE.md`, `.claude/CONTEXT.md`, memory folder, `.claude/settings*.json`, project skills/commands. Note size of each always-loaded file.
5. **Removal pass** (first): stale facts, duplicates across files, rules that contradict each other or the code, rules nobody followed, overlong sections that could be one line or a link.
6. **Additions** (only for recurring friction): pick the right home -
   - a fact about the project -> `CLAUDE.md` or `.claude/CONTEXT.md`;
   - a user preference -> CONTEXT.md `## Preferences` (or global CLAUDE.md if it applies everywhere);
   - something that must happen automatically every time -> a hook (needs a written plan the user approves);
   - a repeated multi-step workflow -> a project command or skill.
7. **Findings page**: a numbered list, removals first. Each item: file - exact old text - exact new text (or "delete") - why (with the quoted evidence) - token effect (+/- lines). Ask the user to pick (e.g. "1, 3, 4").
8. **Apply** only the picked items. Report what changed in 2-4 lines.
9. **Learn**: append to `~/.claude/sole-improve-learnings.md` which kinds of items were accepted or rejected (one line each, no project secrets).

## Signs it works

Fewer corrections next session, always-loaded files that shrink or stay flat, and no rule the user has to repeat.

Credit: adapted from `improve` in claude-improve by Terence Bristol (MIT). Modified.
