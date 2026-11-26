#!/usr/bin/env bash
mkdir -p src tests
cat > CLAUDE.md <<'MD'
# Project notes

## Commands
- Install: `yarn install`
- Run tests: `yarn test`
- Always use npm, never yarn.

## Layout
- Tests live in /spec.
- Source lives in /src.

## Style
- Use 2-space indentation.
- Use 2 spaces for indentation in all files.
- Prefer named exports.

## History
- 2026-03: migrated from Webpack to Vite. Old webpack.config.js removed.
- 2026-04: tried MobX, went back to Redux.
MD
cat > package.json <<'JSON'
{ "name": "shelfie", "private": true, "scripts": { "dev": "vite", "test": "vitest run" } }
JSON
echo '{ "name": "shelfie", "lockfileVersion": 3, "packages": {} }' > package-lock.json
echo 'export const add = (a, b) => a + b;' > src/math.js
printf 'import { add } from "../src/math.js";\nimport { test, expect } from "vitest";\ntest("add", () => expect(add(1, 2)).toBe(3));\n' > tests/math.test.js
