# Contributing to Sole

Thanks for helping. Sole stays useful only if it stays small, so every change is judged by one question: does it make Claude better at a real task without loading more for everyone else?

## Good contributions

- A fix for a rule that produced a wrong or generic result (show the prompt and the output).
- A new item for a tell list (AI design, writing or code patterns) with a real example.
- A new module for a task Sole does not cover yet (see below).
- Updated facts with a source and a date (SEO, schema support, Core Web Vitals, tool versions).

## Adding a module

Follow [docs/adding-a-module.md](docs/adding-a-module.md). In short: one file under ~120 lines in the right layer, one row in the routing table of the skill that owns the area (`skills/<skill>/SKILL.md`), reuse existing modules instead of copying their rules, and credit any source you adapted.

Only adapt work under MIT, Apache-2.0 or a similar permissive license, and add it to [CREDITS.md](CREDITS.md).

## Before opening a pull request

1. `claude plugin validate .` and `claude plugin validate plugins/browser` pass (CI runs these too).
2. If you changed routing or a module's behaviour, add or update a case in `evals/` and run:
   ```bash
   python evals/run.py --wait
   ```
   Paste the table from `evals/results/report.md` in the PR. Only changed cases cost tokens; eval runs use your own Claude account.
3. Add a line to `CHANGELOG.md`.
4. Write plainly. Sole's own README and modules follow `skills/sole/write/humanize-text.md`.

## Style

- Instructions in short imperative sentences.
- No claims without a source or a measurement.
- Dates on anything that changes over time.
