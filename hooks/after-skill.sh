#!/usr/bin/env bash
# Sole PostToolUse hook for the Skill tool.
# Right after a Sole skill loads, print the absolute path of the shared module library and remind
# Claude to read the module the skill's table names before answering. In tests Claude sometimes
# answered from the skill file alone and missed the module's rules. Prints nothing for any other
# skill. Reads the hook input from stdin only.
input=$(cat)
skill=$(printf '%s' "$input" | grep -Eo '"skill"[[:space:]]*:[[:space:]]*"sole:(sole|code|visual|write|business)"' | head -n 1 | sed -E 's/.*"(sole:)([a-z]+)"$/\2/')
[ -n "$skill" ] || exit 0
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
# JSON-escape backslashes and quotes in the path (Windows paths contain backslashes).
lib=$(printf '%s' "$root/skills/sole" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g')
if [ "$skill" = "code" ]; then
  note="If a row of its table matches, Read that module from the library before you answer; otherwise follow the skill file."
else
  note="Before you write any answer, Read the module its table names from the library. Do not answer from the skill file alone: the module holds the checklist the answer must follow."
fi
printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"Sole %s loaded. Sole library: %s. %s"}}\n' "$skill" "$lib" "$note"
exit 0
