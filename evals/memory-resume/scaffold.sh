#!/usr/bin/env bash
mkdir -p .claude
cat > .claude/CONTEXT.md <<'MD'
# Project context
Last updated: 2026-11-10

## Goal
Website for "Hilltop Roasters", a specialty coffee roaster in Bristol.

## Preferences
- Keep replies to three sentences or fewer.
- No purple, no Inter font.

## Decisions
- Palette: roasted brown #4A2C1D, crema #E8D3B0, green-bean #6B7F3A - 2026-11-08

## Done
- Homepage built (index.html) - 2026-11-09

## Next
1. Build the pricing page (subscription tiers: 250 g / 500 g / 1 kg).
2. Write workshop booking copy.

## Reminders
- Owner wants the Saturday workshop price shown as £45.
MD
