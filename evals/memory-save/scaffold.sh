#!/usr/bin/env bash
mkdir -p .claude
cat > .claude/CONTEXT.md <<'MD'
# Project context
Last updated: 2026-11-15

## Goal
Orders service for the Steep & Co shop.

## Preferences
- Short answers.

## Decisions
- REST, not GraphQL - 2026-11-12

## Done
- Order model and API skeleton - 2026-11-14

## Next
1. Pick a database.

## Reminders
MD
