---
description: Get a specialist's view or deliverable from the Agency Agents persona library (fetched on demand)
argument-hint: "<role or task> [what to review or produce]"
---
Invoke the Skill `sole:sole` first (its result gives the skill's base directory), then read from that directory and follow `personas.md` for: $ARGUMENTS

Pick the best-matching persona from the index (or ask if two fit), fetch only that file, and run it as a subagent. The persona's invented background is never presented as fact.
