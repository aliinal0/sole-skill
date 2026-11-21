# Deslop UI - interfaces that look designed, not generated

AI UI looks generic for two reasons: no constraints (the model falls back to the statistical average of web code) and designing before knowing what the thing is. Fix both: strategy first, then a system, then craft, then a check.

**The brief wins.** A look, era, font or palette the user pinned beats every rule here, including the tell lists.

## Pick the job

| Request | Do |
|---|---|
| New page/app/screen, or a redesign | Phases 0-3 below |
| A named refinement ("polish", "make it bolder", "fix the typography", "critique this") | `build/design/commands.md` -> that verb only |
| "Make it look like <brand>" / "in the style of X" | `build/design/references.md` (transpose, never clone) |

**Refinement preserves, redesign replaces.** A refinement keeps the existing identity, copy and behaviour. A redesign keeps product truth and content but treats the old look as an anti-reference. Never polish a look you were asked to replace.

## Phase 0 - Know what you are designing

If `DESIGN.md` (and `PRODUCT.md`) exist at the project root, read them and follow them. Skip questions they answer.

Otherwise settle with `core/intent.md`:
1. **Mode** of the surface - what success looks like for the visitor:
   - **Persuade** (landing, pricing, campaign): they decide and act. Full commitment, a point of view.
   - **Operate** (app, dashboard, admin, editor): they finish a task. Precision and known patterns beat expression.
   - **Read** (docs, articles, help): they understand. Structure, then a reading experience worth staying in.
   - **Experience** (portfolio, gallery): the work leads, the interface recedes.
   Pick from the surface, not the company: a dev tool's landing page is still Persuade.
2. **Kind of business** for marketing sites - it decides the page plan: `build/design/page-kinds.md`.
3. **Who and why**: audience, positioning, the one primary action.
4. **Words before pixels**: 3-5 adjectives and a 3-word essence.
5. **Subject matter**: the trade's materials, objects, vocabulary and real photos are where distinctive choices come from.

## Phase 1 - Plan, then check the plan

Write a compact plan before code:
- **Colour**: 4-6 named values (OKLCH preferred): one dominant, one sharp accent, neutrals, success/warning/error, about 60-30-10. Light or dark chosen from the use scene (who, where, what light), not the category.
- **Type**: 1-2 families with clear roles, sourced and self-hosted when possible; a modular scale with a stated ratio.
- **Layout**: one-sentence concept + ASCII wireframe; alignment decided.
- **Signature move**: the one memorable thing. Everything else stays quiet.
- **Tokens**: spacing unit, max two radii, one elevation approach (border OR shadow).

Then ask: "Would I produce this same plan for any similar brief?" Revise every part that says yes, and say what changed.

## Phase 2 - Build to the craft floor

Read `build/design/craft-floor.md` right before editing UI code (not for planning-only answers). It holds the verify list, the refuse list and the accessibility gate. Build without announcing the checklist.

Copy: `write/docs-copy.md`. Visual assets: `build/deslop-media.md`.

## Phase 3 - Record and check

1. Write or update `DESIGN.md` from `templates/DESIGN.md`. Later sessions read it instead of re-asking.
2. Look at the rendered result at the sizes it ships (1440, 1024, 768, 390): `build/browser-checks.md` -> "Render check" and "Console and network errors" when the browser plugin is installed. Batch the fixes per look.
3. Run the `critic` agent with `build/design/craft-floor.md`. Fix what fires.
4. Remove one accessory before shipping.

Credit: adapted from `frontend-design` (Anthropic, Apache-2.0), `frontend-design-deslop` (Samuel Berthe, MIT), Impeccable (Paul Bakaus, Apache-2.0) and taste-skill (Leonxlnx, MIT).
