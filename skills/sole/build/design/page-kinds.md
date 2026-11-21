# Page plan by kind of business

**Scope: marketing websites only (Persuade mode).** Never apply these rules to app UI, dashboards, admin screens or docs - those follow Operate/Read mode in `build/deslop-ui.md`.

Write the kind on the first line of the plan. It decides what leads every screen.

| Brief | Kind | Leads with | Effects allowed |
|---|---|---|---|
| App, SaaS, AI, developer tool, fintech app | software | The product's own UI as live HTML doing its real job (a code-review tool shows a real diff with Accept) | One effect (shader ground, WebGL part or scene) + 1-2 moments |
| A game | gaming | Its name in the H1, its world as full-bleed key art | Same as software; the effect never replaces the art |
| Hardware, a device | tech | Real product photos (stand-ins of its kind if none), big and whole | One effect only if the brief asks for 3D |
| Other physical product or brand | product | Photos: the product big, a different view each section, every headline promise pictured | None. Photos, flat colour, type |
| People are hired: clinic, law firm, agency, studio, trade | service | Photos of the people, the rooms, the work; real icons of tools they use | None. One still diagram at most |
| People come to it: cafe, bakery, shop, hotel, gym | place | Photos (12-20 on a full page); visit info on screen two; address or name set large as the type moment | None. No grounds, loops or diagrams |

A maker that also opens its door (a bakery with a web shop) is a **place**.

## House rules (all kinds)

1. One section per screen at 1440x900; the hero alone on the first screen.
2. Equal left and right content edges.
3. Every visual renders at 1440, 1024, 768 and 390 - never an empty frame.
4. No visible captions under images; photo credits in one footer line. Every image still gets meaningful `alt` text.
5. Quiet micro-interactions: linked cards lift ~2 px, photos zoom 1.02-1.03 in their frame, buttons step on hover and press on click. No tilt, carousels or auto-rotating tabs.
6. One hero entrance on load, plus one "moment" per page (two on long pages): a photo- or type-led composition that breaks the rhythm once. This is the "one authored moment" of the craft floor, not an extra animation layer.
7. Logos of real tools and integrations appear in their own colours; never a drawn look-alike of a real logo. Interface icons (menus, buttons, features) still come from one consistent icon set, as the craft floor requires.
8. Software pages: about 60-80 words per screen outside UI mock-ups.
9. Placeholder contacts: street and district only, `.example` emails, no real-format phone numbers.

## Never

- One object carrying the whole page: the hero object leads at most two more sections; other visuals carry the rest.
- Stock photos passed off as the client's product, people or place.
- Violet/lavender as the page's own accent unless the brief or brand demands it.
- Copying a reference site's code, copy, images or signature effect.

Credit: condensed from taste-skill by Leonxlnx (MIT). Modified.
