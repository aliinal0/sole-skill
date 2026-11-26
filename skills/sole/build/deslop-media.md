# Deslop media - images, thumbnails, generator prompts

Applies to prompts for image or video generators, thumbnails, covers and still graphics. Editing real footage: `build/video/edit.md`. Motion graphics and promo films: `build/video/motion.md`.

## Before generating

Settle with `core/intent.md`: platform and aspect ratio, audience, the single message, 3 style adjectives, one reference the user likes.

## Visual AI tells to avoid

- Over-smooth, plastic skin; perfect symmetry; glossy "everything lit from everywhere" lighting.
- Default cinematic teal-orange grade, heavy bokeh, lens flares on everything.
- Floating abstract shapes, glowing particles, holographic UI, robots/brains for "AI".
- Text inside generated images (garbled letters); add text in the edit instead. That includes objects that carry writing: labels, signs, menus, book spines.
- Hands, crowds, reflections and backgrounds that do not hold up on a second look - crop or regenerate.

## Make it read as made by a person

- **Specific over generic**: name real materials, places, times of day, lenses (35 mm, eye level), imperfections (dust, fingerprints, worn edges).
- **Say what you want, not what to avoid**: words like "no bokeh" or "avoid lens flares" inside the prompt often produce exactly that. Describe the wanted look instead (f/8, deep focus, clean lens), and put exclusions in the tool's separate negative-prompt field when it has one.
- **Room for a headline** means one plain, dark or light surface on that side: no window, lamp, prop or person there.
- **Scene, not story**: props and light that fit the place are fine; people, products or places the user did not mention are not.
- **One art direction** for the whole set: palette, grain, lighting direction, framing rules. Write it down (in `DESIGN.md` if one exists).
- **Real material first**: product screenshots and real photos beat generated stand-ins.
- **Thumbnails**: one subject, one idea, readable at phone size; real faces and real product over generated drama; no fake arrows, red circles or shocked faces unless the creator's style uses them.
- **Captions and on-image text**: write them with `write/humanize-text.md` rules.

## Honesty

Generated images of realistic people or events follow the platform's disclosure rules. Never remove AI watermarks or content credentials, and never present generated images as real photos of real events.

## Check

View at real size and on a phone. Run the `critic` agent with this file's tell list.
