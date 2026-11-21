#!/usr/bin/env bash
# Sole PostToolUse hook for the Skill tool.
# Right after the Sole router loads, remind Claude to read the module the routing table names
# before answering. In tests Claude sometimes answered from the router alone and missed the
# module's rules. Prints nothing for any other skill. Reads the hook input from stdin only.
input=$(cat)
printf '%s' "$input" | grep -Eq '"skill"[[:space:]]*:[[:space:]]*"(sole:)?sole"' || exit 0
cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"Sole router loaded. Before you write any answer, Read the module that Step 1 of the Sole skill names for this request (from the skill's base directory). Do not answer from the router alone: the module holds the checklist the answer must follow."}}
JSON
exit 0
