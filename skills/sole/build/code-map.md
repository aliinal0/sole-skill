# Code map - understand a big codebase without re-reading it

Re-exploring a large repo every session is the biggest silent token cost. Build a map once, then query it.

## 1. Use what exists

- `graphify-out/GRAPH_REPORT.md` or `graphify-out/graph.json` exists -> answer architecture questions from it first (`graphify query "<question>"` if the CLI is installed). Read source only to confirm.
- `.claude/CODEMAP.md` exists -> read it first.
- One targeted lookup ("where is X defined", "what calls Y") in a normal-size repo -> just `Grep`; no map needed.

## 2. Build a map when it pays off

Build one when many questions will hit the same codebase, the repo is large (roughly > 200 source files), or the user asks.

**Option A - graphify (rich, optional, external tool).** A knowledge-graph tool: tree-sitter AST + call graph locally, plus model-based extraction for docs/PDFs/images. Install needs Python 3.10+ and the user's OK:
```bash
pip install graphifyy && graphify install
```
Then `/graphify .`. Code extraction is local and free; semantic extraction of docs/images costs tokens - say so before running it on a docs-heavy folder. Its outputs go to `graphify-out/`; suggest adding that to `.gitignore`.

Tell the user before installing: graphify's own installer also adds its own `/graphify` skill, a section in `CLAUDE.md`, and a hook that runs before every file search. That is graphify working as designed and does not break Sole (this module simply defers to graphify's map), but it is a change to their setup they should agree to. To undo it, uninstall graphify and remove that CLAUDE.md section and hook.

**Option B - lightweight CODEMAP (built in, no install).** Launch 2-4 Explore/general-purpose agents in parallel, one per top-level area. Each returns <= 40 lines. Merge into `.claude/CODEMAP.md`:

```markdown
# Code map - <repo>  (updated YYYY-MM-DD, commit <short-sha>)
## Stack
## Entry points          (path - what starts here)
## Modules               (path - responsibility - key files - depends on)
## Data flow             (request/job path in 3-6 steps)
## Conventions           (naming, errors, tests, where new code goes)
## Hot spots             (big/complex/fragile files)
## Glossary              (domain terms -> code names)
```

Keep it under ~150 lines. Link files; do not paste code.

## 3. Keep it fresh

- After a change that moves modules or adds an entry point, update the relevant lines (graphify: `graphify . --update`).
- Put the map's path in `.claude/CONTEXT.md` -> `## Key files` so the memory hook points future sessions to it.
- If the map and the code disagree, the code wins; fix the map.

Credit: graphify by Safi Shamsi (Apache-2.0) is integrated as an optional external tool, not bundled.
