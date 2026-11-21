#!/usr/bin/env bash
mkdir -p .claude
cat > .claude/VOICE.md <<'MD'
# Voice profile
Samples used: 5 (emails) | Updated: 2026-11-02
Language(s): English (British)

## Rhythm
- Typical sentence length: short, 5-12 words.
- Paragraph length: 1-2 sentences.
- Mix of short/long sentences: mostly short.

## Tone
- Formality (1-5): 2
- Humour / warmth: dry, warm
- Directness: says it straight, no hedging

## Habits
- Typical openings: "Hi <name>," then straight to the point.
- Typical closings: "Cheers, Dana"
- Punctuation habits: no exclamation marks, no emoji, no dashes; commas and full stops only.
- Words and phrases they use: "a bit", "reckon", "sorted", "shout if"
- Words and phrases they never use: "excited", "thrilled", "reach out", "circle back", "apologies for any inconvenience"

## Do / don't
- Do: British spelling (organise, colour). Put the ask in the second line.
- Don't: apologise more than once.
MD
