# Deep research - split the work across agents

Use when a question needs many sources, a comparison or a report. For a single fact, just search.

## 1. Plan as a dependency graph

Break the question into 4-8 sub-questions (max 12). Each must be answerable by someone with no other context in 1-3 searches.

```
| ID | Sub-question | Depends on |
|----|--------------|------------|
| q1 | ...          | -          |
| q2 | ...          | -          |
| q3 | ...          | q1         |
```

Show the table, then start. Do not wait for approval unless the scope is unclear (then use `core/intent.md`).

## 2. Fan out in waves

- **Wave 1**: every node with no dependencies -> one `researcher` agent each, **all launched in the same message** (parallel).
- **Wave 2+**: nodes whose dependencies are done; paste the dependency findings into their brief.
- Each agent returns only: Findings (with inline sources), Gaps, Sources. This keeps the main context small.
- After each wave, append sources to `.claude/sole/research/<topic-slug>-sources.json` so they survive a context reset.

## 3. One gap round, max

Collect the gaps. If a gap could change the conclusion, run 1-3 targeted follow-up agents in one final wave. Otherwise skip. Never loop.

## 4. Synthesise

Write from `templates/research-report.md`:
- Summary first (3-5 sentences, the answer).
- Findings by theme, not by agent. Resolve contradictions or state them.
- Confidence and open questions, honestly.
- Deduplicated sources.

Save to `docs/sole/research/YYYY-MM-DD-<topic-slug>.md` (ask once before the first report goes into the project). Give the user the summary in chat plus the file path.

## Cost control

- Simple comparison: 3-4 agents. Broad market study: up to 8 + 1 gap wave.
- Agents fetch at most 3-5 pages each; use `research/web-access.md` for blocked ones.

Credit: wave/DAG pattern adapted from `deep-dive` by Rohit Ghumare (Apache-2.0) and `deep-research` by daymade and Samuel Berthe (MIT).
