---
disable-model-invocation: true
description: Get a specialist's view or deliverable from the Agency Agents persona library (fetched on demand)
argument-hint: "<role or task> [what to review or produce]"
---
Invoke the Skill `sole:sole` first (the hook after it prints the Sole library path), then read from the library and follow `personas.md` for: $ARGUMENTS

Pick the best-matching persona from the index (or ask if two fit), fetch only that file, and run it as a subagent. The persona's invented background is never presented as fact.
