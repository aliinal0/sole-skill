# Humanize text - remove signs of AI writing

The tell lists below are for English text.

## Method

1. **Mark the tells**: read the whole text once, mark every pattern below, strongest first. Look at paragraph shape too, not only sentences.
2. **Rewrite**: keep every fact, name, number, date, quote and claim. You may shorten, merge, reorder. Where the text is generic, make it specific using only facts already in the text or given by the user; otherwise write a simpler sentence. Never invent facts, numbers, limits or examples. A sentence that only praises ("an indispensable address", "loved by many") either goes or keeps its claim as it is; never swap it for a new claim about customers, popularity or results ("many regulars now..."). Do not explain what a feature does beyond the source either: "integrates with Slack" may become "works with Slack", never "log hours from Slack".
3. **Check**: did any fact change or vanish? Then read it as a stranger: what still sounds generated? Re-check the survivors: contrasts, closers, triads, dashes, bold labels.
4. **Final**: state each point plainly. Vary sentence length. If a sentence stays awkward, rewrite the paragraph around its main point.

**Return only the rewritten text.** No notes, no "what I changed", no explanation, no quoted fragments of the original, unless the user asked for them (cleanup or report mode). Never add a detail that is not in the original, not even with a warning; if a sentence needs one, write the simpler sentence instead.

## Modes

| Request | Mode | Output |
|---|---|---|
| "humanize / rewrite this" (default) | **rewrite** | The clean text only |
| "suggest edits I can accept" | **cleanup** | Numbered edits: original span -> replacement -> pattern # |
| "audit / check before publishing / flag only" | **report** | Issues found (span, pattern #, severity, why) + a short assessment; original untouched |
| "learn my voice" | **teach** | Build `.claude/VOICE.md` from `templates/VOICE.md` using 3+ samples the user wrote (ask for them, or read files they point to) |
| "write this in my voice" | **mimic** | Draft using `VOICE.md`; then run the patterns below on the draft |

If `.claude/VOICE.md` exists, every rewrite also matches it (sentence length, openings, formality, words they use and never use).

Strict check (on request): give before/after pattern counts and the share of text changed. More than ~40% changed on a "light edit" request means you over-edited.

## Patterns

**A. Staging instead of stating**
1. "Not X, but Y" / "It's not just X - it's Y" contrasts.
2. One-line dramatic closers and fragments ("And that changes everything.").
3. Fake-deep sayings ("Great design is invisible.").
4. Run-up before the point ("Here's the thing:", "Let's dive in").
5. Arguing with an imaginary objector.

**B. Rhythm by rule**
6. Forced groups of three.
7. Repeated sentence openings.
8. Em dashes as the universal connector.
9. Stacked qualifiers ("truly", "incredibly", "deeply").
10. Hyphenated word pairs everywhere ("fast-paced, ever-evolving").
11. Passive voice with no actor.

**C. Inflation and borrowed authority**
12. Overused words: delve, leverage, seamless, robust, elevate, unlock, empower, tapestry, landscape, realm, pivotal, crucial, testament, game-changer, navigate (figurative), foster, streamline.
13. Inflated significance ("plays a pivotal role in shaping...").
14. Vague links ("is associated with", "is linked to") without saying how.
15. Shallow -ing tails ("..., highlighting its importance").
16. Sales language in neutral text.
17. Vague authority ("experts say", "studies show") with no source.
18. Avoiding plain *is / has* ("serves as", "boasts", "stands as").

**D. Formatting by rule**
19. Bold used as decoration or as label-colon at the start of every bullet.
20. Headings on a text too short to need them.
21. Curly quotes / emoji / ✅ in plain contexts that do not use them.

**E. Chat leftovers**
22. "Great question!", "I hope this helps", "Certainly!", "Let me know if...".
23. Knowledge-cutoff disclaimers and hedged guesses.
24. First sentence repeating the heading.
25. Writing about the document ("This article will explore...") instead of the subject.

**F. Wrong reader**
26. Re-explaining what the reader already knows.

**G. Plain speech**
27. Synonym cycling: "the protagonist... the main character... the hero" for one thing. Pick one word and repeat it.
28. False ranges: "from X to Y" where X and Y are not on one scale. List the items.
29. Colons as mid-sentence connectors and title-case headings. Use sentence case; colons only before a list or example.
30. Abstract metaphor nouns: landscape, paradigm, north star, flywheel, surface (as in "API surface"), substrate, vector (as "way"), nexus, bedrock. Use the concrete word.
31. Says how it feels, not what it does: "types that follow your schema" -> "a column rename fails the build". If the sentence could appear unchanged in another product's docs, it says nothing; cut or make it specific.
32. Filler and hedging: "in order to" -> "to"; "due to the fact that" -> "because"; "could potentially" -> "may"; "It is important to note that" -> delete.
33. Adverbs propping weak verbs ("significantly improves") -> the number or a stronger verb; fancy words (utilize, leverage, facilitate, numerous) -> use, help, many.
34. Mannered prose: aphorisms, personified code ("the plan holds it"), figurative verbs ("rides along"). Say it literally.
35. Over-compression in written deliverables: dropped articles, arrows, symbol-speak. Docs and posts get whole sentences (lean mode is for chat only).

## When not to act

Do not "fix" legal, scientific or technical text where precise, formal wording is required. Do not touch quotes, code, names or the user's deliberate style. Good human writing sometimes uses a dash or a list of three; remove patterns only when they are the default, not a choice.

Credit: pattern catalogue adapted from `humanizer` by Siqi Chen (MIT), itself based on Wikipedia's "Signs of AI writing" guide; modes, voice profile and group G from `unslop` by Clayton Kim (MIT, per its skill metadata) and `unslop` in pstack by Lauren Tan (MIT). Modified.
