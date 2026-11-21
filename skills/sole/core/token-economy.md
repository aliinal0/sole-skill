# Token economy

Most tokens are spent on **input** (files read, tool output, chat history), not on the reply. Cut both, input first.

## Input side (biggest savings)

1. **Load less.** Read only the module and file sections you need. Use `Grep` / `offset`+`limit` before reading whole files.
2. **Delegate wide reads.** Searches across many files or many web pages go to a subagent. Keep its summary, not its transcript.
3. **Memory over re-reading.** After a reset, read `.claude/CONTEXT.md` instead of re-exploring the repo or the chat.
4. **Trim tool output.** Pipe long commands through `head`, `tail`, `grep`; ask for `--quiet` flags; never dump lockfiles, logs or minified files.
5. **Do not re-read** a file you just wrote or edited.

## Output side

- Answer first: `[thing] [action] [reason]. [next step].`
- No greeting, hedging, recap, sign-off, or "let me...".
- Short words over long phrases. Fragments are fine when the meaning stays exact.
- Code changes: changed lines + 1-2 lines of context.
- Between routine tool calls: no text. One line per phase, one line with the result.

## Lean mode (`/sole:lean`)

Applies the output rules harder for the rest of the session: drop articles and filler where the sentence still reads in one pass. Stays on until the user says "normal mode".

A lean answer is the direct answer plus the fix in about 2-5 short lines, roughly 60 words of prose at most (code not counted). Leave out side cases, background, alternatives and extra tips unless the user asks; offer them in a few words at most ("more: X, Y") or not at all. No closing sentence offering help.

Never compress:
- negations and limits (`not`, `never`, `only`, `except`), numbers, units;
- code, commands, paths, error messages (keep verbatim);
- security warnings, irreversible actions, questions to the user, step order;
- anything saved outside the chat: code, comments, commits, docs, CONTEXT.md.

If a compressed sentence could be read two ways, write it in full.

## Honest expectations

Output compression alone typically saves a small share of a bill, because input dominates. The input rules above matter more.

Credit: output rules adapted from `caveman` by Julius Brussee (Apache-2.0).
