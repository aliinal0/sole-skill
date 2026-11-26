# Adding a module

1. **Pick the layer** in the library (`skills/sole/`): `build/`, `business/`, `research/` or `write/`. If it applies to every request, it belongs in `core/` (rare).
2. **Create `skills/sole/<layer>/<name>.md`**, under 100 lines:
   - one-line goal;
   - "Before starting": only the questions that change the result;
   - the method as numbered steps;
   - which shared agents to launch and with what brief;
   - output format;
   - `Credit:` line if you adapted someone else's work.
3. **Add one row** to the routing table of the skill that owns the area: `skills/code/`, `skills/visual/`, `skills/write/`, `skills/business/` or `skills/sole/` (`SKILL.md`). Make the trigger phrase distinct from existing rows. Paths in the table are library paths.
4. **If the module needs a new trigger area**, extend that skill's `description` with a few words. Keep it under 1,024 characters (the runner checks). Do not edit the Shared rules block in one skill only; change it in all five.
5. **Reuse, do not duplicate**: link to existing modules (`write/humanize-text.md`, `research/web-access.md`) instead of copying their rules.
6. **New agent?** Only if no shared agent fits. Put it in `agents/`, keep it single-purpose, and give it a fixed short return format.
7. **Credit and license**: add a row to `CREDITS.md` for any adapted source; only adapt MIT, Apache-2.0 or similarly permissive work.
8. **Test**: add a case in `evals/<name>/case.yaml` with a `tool_used` grader for the module and an `llm` grader whose criterion states the source facts (the judge sees only the criterion and the final answer). Run `python evals/run.py --case <name>`; only changed cases cost tokens.
