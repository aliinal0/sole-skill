# Motion graphics - promos and launch films that look directed

For launch videos, product promos, feature reveals, brand stings, kinetic type and animated explainers built in code (Remotion, HyperFrames, HTML + ffmpeg) or in After Effects. Real camera footage: `build/video/edit.md`.

If the user has the full `motionmaxxing` skill installed, use its scripts and gates; this file is the short version. A look or element the user explicitly asks for overrides the lists below.

## 1. Decide before animating

1. **One true thing**: in four lines, the problem, the audience, the goal, the feeling; then the one feature or moment this film is for.
2. **Three ideas of different kinds** (a documentary of one real task, a held shot, a joke with a character, a typographic essay, a montage of real output). Drop the first idea if it is the name's first association (a rocket for "launch", stars for a star name).
3. **Cover-the-logo test**: with the logo and colours swapped, would this be the same film for a competitor? Then it is not an idea yet.
4. **Storyboard**: each beat as "Buys: the viewer believes ___". Cut any beat that buys nothing. Proof gets the largest share of the time.

## 2. What good looks like

- **Show, then say**: a claim in type is followed by the product doing it, with real UI and real content.
- **Every beat causes the next**: the last frame of one beat becomes the first of the next; a hard cut means something.
- **Spend emphasis**: one lit thing per frame; at most a quarter of the beats are "the point"; endings get smaller.
- **Time breathes**: hold before what matters, give reading its time, stop before the idea is spent.
- **One world**: one logic of light, material, lens and type, from the brand. A background is a surface, not a flat colour swatch.

## 3. Motion craft (measured on professional films)

- Cut on motion, never on rest; scenes start already moving.
- Entries decelerate (most travel in the first 4-8 frames, then a long tail, no bounce); exits accelerate out. A typical move lasts about 10 frames (0.33 s at 30 fps). At most one visible spring per film.
- Almost nothing fades between scenes; things arrive by moving, cutting, unmasking or focusing.
- Words land at speech rhythm: whole words 2-12 frames apart. Letter-by-letter typing only inside the product's own input field.
- No dead frame: a held frame keeps one living thing. A designed pause of 0.6-1.5 s before a payoff is good.
- A UI demo is physical: the cursor parks before it clicks, the press squashes 2-3 frames, the target answers a frame later.
- One system per film: one frame clock, one blur style, the brand's type, one accent colour with one meaning.

## 4. Never ship

1. Corner labels, counters ("01 / 04"), timecodes, progress bars, scene titles over a shot.
2. Slide-deck layouts: a held headline on the left with a device on the right, a small label above every headline.
3. Generic web cards with status dots and invented values where real UI exists.
4. Invented stats, stat slides (big number over a small label), on-screen disclaimers. The same goes for any product fact the brief did not give (platforms, prices, integrations, customer names, "available now"): leave it out or mark it `[confirm: ...]`.
5. Slogan copy: one-word triplets, "Not just X. It's Y.", "Unlock", "Meet X", "the future of".
6. The house style as a default: a giant cropped word, a colour flood or circle wipe between every beat, a dot that becomes the logo, everything moving all the time.
7. A small card on an empty background, or the same object pinned in place for three shots.
8. A web-footer ending (logo + tagline + button + URL) or an end card held past ~1.4 s.
9. A render you did not watch.

## 5. Sound

Silence before the hit; pull music down while the viewer reads; one to three hand-placed hits on real events; voice-over at about 2.5-3 words per second with on-screen words landing just before they are heard. Licensed or generated-with-permission audio only.

## 6. Check the render

Watch it at full size and on a phone. Check: no blank or frozen stretch over ~0.1 s, end hold 0.6-1.4 s, the final shot under a quarter of the film, UI text readable, one hero per frame. Run `scripts/video_check.py` for loudness and rhythm, and the `critic` agent with `build/video/tells.md`. Deliver the video, the editable source and a short note: the idea, what each beat buys, and what is real versus illustrative.

Credit: condensed from motionmaxxing by Tejashmakwana (Apache-2.0): judgments, craft laws, never-ship list and gates rewritten and shortened. Modified.
