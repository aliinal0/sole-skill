---
disable-model-invocation: true
description: Check a page in a real browser - render at breakpoints, console errors, accessibility, performance (needs the sole-browser plugin)
argument-hint: "<url or localhost address> [render | a11y | perf | seo | all]"
---
Invoke the Skill `sole:code` first (the hook after it prints the Sole library path), then read from the library and follow `build/browser-checks.md` for: $ARGUMENTS

Default is `all`. If no chrome-devtools tools are available, say that the sole-browser plugin is needed and what it would check.
