# Design commands - targeted refinements

Use when the user names one of these (or clearly means it), e.g. `/sole:design polish src/pages/home.tsx`. Run only that verb. A refinement keeps the existing identity, copy and behaviour unless the verb says otherwise. Read `build/design/craft-floor.md` before editing.

If no verb is given, show this table and ask which one; never auto-run.

## Plan and document

| Verb | Do |
|---|---|
| `shape` | Plan UX/UI before code: users, jobs, flows, screens, states. Output an ASCII wireframe per screen + open questions. No code. |
| `init` | Write `PRODUCT.md`: what it is, for whom, mode per surface, voice, constraints. |
| `document` | Read the existing code and write `DESIGN.md` from what is really there (tokens, type, components). |
| `extract` | Pull repeated values and components into tokens and shared components; no visual change. |

## Evaluate (report first, change nothing)

| Verb | Do |
|---|---|
| `critique` | UX review. Score 1-5 each: hierarchy, clarity of primary action, consistency, feedback/states, accessibility, distinctiveness vs. category default. Top 5 fixes with location. For distinctiveness, list each template default you find (gradient text, eyebrow labels, identical cards, fake numbering, a lone default font, glass...) with its location and fix; do not fold them into one line. Use the `critic` agent for an independent view. |
| `audit` | Technical check: accessibility (WCAG AA), performance (image weight, layout shift, JS size), responsive breakpoints, semantic HTML. Table: issue - location - severity - fix. With the browser plugin, measure instead of guessing (`build/browser-checks.md`: accessibility, performance, render check). |

## Refine

| Verb | Do |
|---|---|
| `polish` | Final pass: spacing rhythm, alignment, type steps, every state, browser surfaces, copy consistency. No new features. |
| `bolder` | The design is safe or bland: commit harder to the signature move, increase scale contrast, one stronger colour decision. |
| `quieter` | Too loud: cut competing accents, reduce motion, unify radii/shadows, more whitespace. |
| `distill` | Strip to the essence: remove sections, options and decoration that do not serve the primary action. |
| `harden` | Production-ready: error, empty and loading states; long text, i18n, RTL if needed; slow network; edge cases. |
| `onboard` | First-run flow, empty states that show the first action, activation in minutes. |

## Enhance

| Verb | Do |
|---|---|
| `typeset` | Fix hierarchy and fonts: scale ratio, weights, measure, line-height, tracking, pairing. |
| `layout` | Fix spacing, grid, alignment and rhythm; one brief-specific layout move. |
| `colorize` | Add strategic colour to a monochrome UI: one accent with a job, semantic states, tinted neutrals. |
| `animate` | Add purposeful motion: one entrance, feedback on actions, transitions that show what changed. Reduced-motion fallback. |
| `delight` | One memorable, on-brand detail (a micro-interaction, a type moment, an empty-state touch). Never at the cost of speed or clarity. |
| `overdrive` | Push past convention for Persuade/Experience surfaces only, with the user's OK. |

## Fix

| Verb | Do |
|---|---|
| `clarify` | UX copy: labels, buttons, errors, empty states (`write/docs-copy.md`). |
| `adapt` | Make it work at every size and input: phone, tablet, desktop, touch, keyboard. Verify with the render check in `build/browser-checks.md`. |
| `optimize` | UI performance: images, fonts, layout shift, bundle size, render cost. Measure before and after (`build/browser-checks.md` -> "Performance / LCP"). |

After any verb: say what changed in 2-4 lines and what was not checked (e.g. "not tested on Safari").

Credit: command set adapted from Impeccable by Paul Bakaus (Apache-2.0). Descriptions rewritten.
