---
disable-model-invocation: true
description: Senior code review of a diff, branch, PR or the whole repo - bugs, risk, scale, missing tests, speed, and what to delete
argument-hint: "[nothing for uncommitted changes | branch | PR | path | repo | shortcuts]"
---
Invoke the Skill `sole:code` first (the hook after it prints the Sole library path), then read from the library and follow `build/code-review.md` for: $ARGUMENTS (if empty, the uncommitted changes, else the last commit; `repo` audits the whole repo; `shortcuts` lists the `shortcut:` ledger). Report only; change no code unless I ask.
