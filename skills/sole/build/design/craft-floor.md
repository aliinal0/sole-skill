# Craft floor

Read right before editing UI. The brief and the committed design world override everything here except lines marked **ban**.

## Verify (on the built result, in one batched look)

- **Contrast**: body text >= 4.5:1, large text >= 3:1. Secondary text on coloured surfaces is tinted from that hue, never plain grey.
- **Spacing**: tight within groups, generous between sections, more space above a heading than below it. One uniform gap everywhere is a tell.
- **Type**: body measure 65-75ch, display no larger than ~6rem, tracking no tighter than -0.04em, clear size and weight steps. Run the real copy at every breakpoint; nothing overflows.
- **Motion**: one authored moment, not one identical entrance on every section. Ease-out from an already-visible state; animate transform/opacity (blur, clip-path, mask when smooth). Respect `prefers-reduced-motion`.
- **States**: default, hover, active, focus, disabled, loading, error, empty, selected. Real content, working controls.
- **Browser surfaces**: theme text selection, caret, scrollbars, focus rings, link underline offset, tabular numerals. The cheapest sign a page was built, not assembled.
- **Depth**: shadows have an offset and a soft blur. A zero-offset coloured glow is decoration.
- **Copy**: the product's own words. Buttons name their action; errors name the problem and the fix.
- **Coverage**: every brief requirement is present and findable within seconds.
- **Accessibility gate (pass/fail)**: keyboard reachable, visible focus, labels on every input, targets >= 24 px, meaning never by colour alone.

## Refuse (defaults, not choices - the brief can earn them back)

Page scaffolds:
- Same-size cards of icon + heading + text as the page structure. Nested cards: always wrong.
- Hero + 3 feature cards + testimonials + CTA as the only structure.
- Hero-metric template: big number, small label, supporting stats, gradient accent.
- **Ban**: a tracked ALL-CAPS eyebrow/kicker above headings.
- Section numbers `01 / 02 / 03` unless the content is a real sequence.
- A modal for a task that needs no interruption.

Surfaces:
- Gradient text; glassmorphism as decoration; coloured side-stripe borders (> 1 px) on cards and alerts.
- Border + wide soft shadow on the same element (ghost card); radius > 16 px on cards; one radius on everything.
- Hard offset shadows (`4px 4px 0`) outside a genuinely neo-brutalist world.
- Monospace as a "technical" costume rather than for code or data.
- System display faces (Arial Black, Impact, platform sans) or Inter/Roboto as the primary voice.
- Emoji or Unicode glyphs standing in for icons; mixed icon sets. Icons: one library, one stroke.
- Decorative grid/stripe backgrounds and radial spotlight glows with no subject behind them.
- Sketchy SVG "illustrations" and doodles; stock people pointing at laptops; gradient blobs; corporate-Memphis.
- Default palettes: purple/indigo/violet gradients; warm cream + serif + terracotta; near-black + one acid-green accent.
- Fade-in on every section, cards fading in on scroll, parallax text, scroll-jacking, bounce easing, pulsing dots on non-live content.

Content honesty:
- Never invent reviews, quotes, customers, logos or figures. Label stand-in photos and illustrative values as such.

The floor holds mechanics; it never picks the direction. With every check green, spend the page on the committed idea.

Credit: condensed from Impeccable's craft floor (Paul Bakaus, Apache-2.0), taste-skill (Leonxlnx, MIT), `frontend-design` (Anthropic, Apache-2.0) and `frontend-design-deslop` (Samuel Berthe, MIT). Modified.
