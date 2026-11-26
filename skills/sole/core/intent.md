# Intent - understand what the user actually wants

Goal: give the user only the result they want, shaped by their own taste. Ask little, ask well.

## 1. Decide whether to ask at all

Act without questions when all three are clear: **what** to produce, **for whom / for what**, and **what "done" looks like**. Otherwise ask.

Never ask about facts you can find yourself (files, code, docs, the web). Look them up, or send a subagent. Only decisions belong to the user.

## 2. Read the stored preferences first

Check `.sole/CONTEXT.md` -> `## Preferences`. Do not ask again about anything recorded there.

## 3. Ask in rounds (decision tree)

Treat the request as a tree of decisions. The **frontier** is every decision you can ask now without guessing an earlier answer.

- Ask the whole frontier in one round, max 4 questions. Count every ask, including an "also tell me..." line and a request for content or files; merge or drop the rest, and make a sensible default for anything left out.
- Use the environment's question tool when there is one (2-4 options each, your recommendation first). Otherwise use this format:

```
Q1 - <title>: <question with options>
-> Recommended: <answer>
```

- Word each question so "yes" accepts your recommendation.
- After the answers, recompute the frontier. Stop when nothing important is assumed.
- Simple task: one round max. Big build or strategy: as many rounds as the tree needs.

## 4. Questions that usually matter

Pick only the ones that change the result:
- Who is it for, and what should they do or feel?
- Which 3 adjectives describe the desired style or tone?
- Any reference they like (site, brand, competitor, past work)? Any they hate?
- Constraints: stack, budget, deadline, platform, language.
- Format and depth of the answer: short list, full report, code only?

## 5. Confirm, then record

Restate the brief in 2-4 lines before large work. When the user states a lasting preference ("always keep it short", "no emojis", "I prefer Vue"), save it to `.sole/CONTEXT.md` -> `## Preferences` (ask once before creating the file).

## 6. Deliver to the brief

- Deliver exactly what was agreed. Note extras in one line instead of building them.
- If you discover the brief was wrong mid-way, stop and ask; do not silently change direction.

Credit: decision-tree rounds adapted from `grilling` by Matt Pocock (MIT).
