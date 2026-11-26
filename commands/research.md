---
disable-model-invocation: true
description: Multi-agent deep research with a saved report
argument-hint: "<question or topic>"
---
Invoke the Skill `sole:sole` first (the hook after it prints the Sole library path), then read from the library and follow `research/deep-research.md` for: $ARGUMENTS

Plan the sub-question table, launch `researcher` agents in parallel waves, do at most one gap round, then write the report from `templates/research-report.md`. Give me the summary and the file path.
