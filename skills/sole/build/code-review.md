# Code review - a diff, a PR or a whole repo

Review like the senior developer who gets paged when it breaks. Order of importance: **correct, safe, holds at the expected load, tested, fast, lean.** Lean still counts: every extra line must be read, tested and fixed later. Report only; change no code unless the user asks.

## 1. Understand before judging

- Scope: what the user names (uncommitted changes, a branch, a PR, files, a folder, the repo). Nothing named: the uncommitted changes, else the last commit. "Audit" or "the whole repo": the repo.
- Read the diff, then the code around it: callers of every changed function, what it calls, its tests. A change can break code it does not touch: when a signature, return value or behaviour changes, grep every caller.
- Whole repo: read the README, build and deploy config, dependency list, entry points (routes, handlers, jobs, CLI) and tests. Go deep where a mistake costs most (user input, money, auth, data writes, shared state), not file by file, and say what you did not read.
- Find the expected load in the repo (README, deploy config): one person running a script, or many users at once. Judge scale against that and say which load you assumed.

## 2. Look for

1. **Bug:** wrong result, crash, missed edge case (empty, zero, last item, rounding, time zones), a caller broken by the change, the same rule applied differently in two places.
2. **Risk:** injection, weak randomness, secrets in code, unchecked user input; data loss from swallowed errors, writes in the wrong order or a missing transaction. Deep security work: `build/security-audit.md`.
3. **Scale:** fine for one user, wrong for many: check-then-write races, a query per item, lists or caches that only grow, O(n^2) on big input, per-process state that must be shared.
4. **Missing test:** risky logic (a branch, a parser, money, security, data writes, a bug fix) with no test that fails when it breaks. One good test, not coverage.
5. **Speed:** big slowdowns are problems; small wins are suggestions.
6. **Lean:** dead code, unused options and config; a helper the repo already has (name its path); a dependency or code the standard library replaces; an interface with one implementation or a wrapper that only passes calls through; near-copies that must change together; one function doing several unrelated jobs (split by job, never by line count).

## 3. Check before you report

- Every finding needs a concrete case: "this input or situation gives this wrong result". No case, no finding.
- Re-read the lines: the caller exists, the value can really be empty, the code really is unused (grep the whole tree, including tests, config and string references).
- A `shortcut: <limit>, <upgrade>` comment is a decision, not a finding, unless the expected load already crosses the limit.
- Propose the smallest fix; prefer fixes that delete code. No new layers or frameworks.
- No style taste, no "consider", no vague worries.

## 4. Output

Plain words and short sentences; explain a technical term the first time. Start with `What this change does:` (or `What this repo does:` plus the load you assumed) in two or three sentences. Then numbered findings across three groups, skipping empty ones, so the user can say "fix 2 and 5":

- **Must fix:** bug, security hole, data loss, breaks at the expected load.
- **Should fix:** risky code without a test, real slowness, duplication, code that should not exist.
- **Nice to have:** small speed-ups, shorter forms.

Each finding: a bold title and `file:line`, then **Problem** (the concrete case), **Fix** (the smallest change) and **If we skip it** (the cost), one or two sentences each. Whole repo: at most 20 findings; say how many smaller ones you left out.

End with `Verdict:` (ship, or what to fix first), `Lean: -<N> lines possible` when lean findings exist, and `Not checked:` for what mattered but you could not read or run. Nothing found: say what you checked and `Looks good. Ship.`

## Shortcut ledger

"What did we defer?", "list the shortcuts": run `git grep -nE '(#|//|/\*) ?shortcut:'` (outside git: `grep -rnE` with the same pattern, skipping dependency and build folders). One row per hit, grouped by file: `<file>:<line> - <what was simplified>. Limit: <...>. Upgrade when: <...>.` Tag a marker with no upgrade trigger `no-trigger`. End with `<N> shortcuts, <M> with no trigger.`

Credit: review order, finding format and the shortcut ledger adapted from `ponytail` (`ponytail-review`, `ponytail-audit`, `ponytail-debt`) by DietrichGebert (MIT).
