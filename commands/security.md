---
description: Defensive security review - quick scan, focused review, or full audit of this codebase
argument-hint: "[quick | full | <path or feature>]"
---
Invoke the Skill `sole:code` first (the hook after it prints the Sole library path), then read from the library and follow `build/security-audit.md`. Request: $ARGUMENTS

- `quick`: Phase 1 only (dependencies, secrets, config).
- `full`: all phases with parallel `security-auditor` agents, independent verification, and a saved report.
- a path or feature: guidance-mode review of just that.
Local and read-only; never probe live systems.
