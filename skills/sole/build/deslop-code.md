# Deslop code - code that reads like a teammate wrote it

## Match the codebase first

Before writing, read 1-2 neighbouring files and copy their conventions: naming, file layout, error handling, test style, import order, comment density. Consistency with the repo beats any general rule below.

## AI tells in code

| Tell | Instead |
|---|---|
| Comments narrating the obvious (`// increment counter`) | Comment only the *why*, or nothing |
| Comments addressed to the reviewer (`// Added this to fix the bug`, `// Updated to use X`) | History belongs in the commit message |
| Banner comments, emoji in logs, `✅ Success!` prints | Plain, quiet logs at the right level |
| Over-abstraction: factory/manager/service for one call site | Inline it; abstract on the third use |
| Defensive checks for impossible states, `try/except` around everything | Validate at the boundary, let real errors surface |
| Generic names: `data`, `result`, `handleClick2`, `utils.ts` dumping ground | Names from the domain |
| Every function documented with the same template docstring | Document public APIs; keep private code self-explanatory |
| Huge single commit, message "Update files" | Small commits, imperative subject saying what and why |

## Writing new code

Follow the smallest-complete-change rules in the `sole:code` skill: reuse what the repo has, no unrequested features, flags or dependencies. READMEs and docs: `write/docs-copy.md` and `write/humanize-text.md`.

## Before handing over

Run the project's own linter/formatter/tests if they exist. Then scan the diff against the table above (or run the `critic` agent on the diff).
