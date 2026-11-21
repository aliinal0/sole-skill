# Video editing - real footage that feels cut by a person

For talking heads, vlogs, tutorials, interviews, podcasts, reels and shorts. Motion graphics and promo films: `build/video/motion.md`. Thumbnails and prompts for image or video generators: `build/deslop-media.md`.

AI edits look alike because tools apply the same defaults to every video: every pause deleted, word-by-word captions, a zoom on every sentence, a whoosh on every cut, stock footage for every noun, one music level throughout. A person edits from the material and from who is talking. The list of tells is in `build/video/tells.md`.

## 0. Style before cuts

- **The user's style wins.** If they ask for a look this file calls a tell (word-by-word captions, punch-ins, sound effects, a fast cut), do it well and do not argue; one short note on a trade-off at most. The rules below are defaults for when nothing was asked.
- If `.claude/EDITSTYLE.md` exists, follow it and skip questions it answers.
- Otherwise ask one round (`core/intent.md`, max 4 questions): platform and aspect ratio, target length, who it is for and what they should feel, captions (yes/no, style), music (yes/no, mood), and one video the user likes the look of (theirs or someone else's).
- "Learn my style": run `scripts/video_check.py` on one or two of the user's finished videos, look at a few frames, and fill `.claude/EDITSTYLE.md` from `templates/EDITSTYLE.md` (ask once before creating it).

## 1. Tools

- Required: `ffmpeg` (`winget install ffmpeg`, `brew install ffmpeg`, `apt install ffmpeg`, or the `imageio-ffmpeg` Python package, which `scripts/video_check.py` finds by itself). `ffprobe` is optional. Ask before installing anything.
- Transcript: word-level timestamps from a local Whisper build (faster-whisper, whisper.cpp) by default; a paid API only with the user's key and OK. Cache it; never transcribe the same file twice.
- If `video-use` or `ffmpeg-skill` is installed, use their helpers instead of writing new commands.
- Work in `<videos>/edit/`: transcripts, `edl.json`, previews, final. Never overwrite source files.

## 2. Process

1. **Inventory**: `ffprobe` every file (duration, fps, resolution, audio). Note vertical clips that will crop.
2. **Transcribe** with word timings. Read the transcript; look at frames only where a decision needs them.
3. **Plan in plain words**: structure, what goes and why, captions, B-roll, music, grade, length. **Wait for the user's OK.**
4. **Cut list** (`edl.json`: source, start, end, reason). Run `scripts/video_check.py --edl edl.json` on it before rendering: it is exact and costs nothing. Then a preview render.
5. **Self-check before showing it**: frames around every cut, audio at every join, loudness, `scripts/video_check.py` (rhythm, pauses, loudness), the `critic` agent with `build/video/tells.md`. Fix, re-render, max 3 rounds; report what is left.
6. **Iterate** on feedback. On final, add what was learned to `.claude/EDITSTYLE.md`.

## 3. Cutting like a person

- **Cut by meaning.** Keep whole thoughts; the cut point serves the sentence, not the silence detector.
- **Keep breath.** Pauses under ~0.5 s stay. Longer ones shrink to ~0.15-0.25 s of air (the longer end after a sentence or before a point). A deliberate pause before a punchline stays whole.
- **Retakes and false starts**: keep the best complete take (usually the last) and cut the restart cue ("let me say that again").
- **Fillers**: keep in casual talk unless they are dead air; tighten in tutorials and ads only if the user wants it. Removing part of a stumbled word usually leaves a visible jump; leave it or cover it.
- **Never cut inside a word.** Pad edges 30-200 ms; 20-30 ms audio fades at every join.
- **Jump cuts**: hide a distracting one with B-roll, or with a small punch-in (about 5-10%) when the creator's style uses it. Not on every cut.
- **Rhythm follows content**: quick for lists and energy, long holds on emotion, proof and laughs. Extend past a laugh; the reaction is the beat. Even shot lengths read as automatic.
- **Split edits**: let audio lead or trail the picture by 0.3-1 s at speaker and scene changes (J and L cuts).
- **When unsure whether to cut, keep the line** and list it in the plan for the user to decide.

## 4. Captions (only if wanted)

- Clean, not verbatim: drop stutters and fillers in the text, check names and product spelling.
- Default: sentence case, phrase chunks of 4-7 words, at most 42 characters per line and at least 5/6 s on screen (Netflix timed-text guidance), no emoji, no per-word colour pops. Word-by-word or bold uppercase only when the creator's style or the user asks.
- Vertical video: keep captions above the bottom quarter to third of the frame and clear of the right-hand button column; the apps change their overlays, so check a current safe-zone template.
- Burn subtitles last in the filter chain so overlays never cover them.

## 5. B-roll

- Use it where it shows what words cannot, or to cover a jump. Not one clip per noun.
- The creator's own footage first. Stock only when asked and never presented as theirs. Generated footage only with the user's OK, and disclosed where the platform requires it.
- Length follows the action (2-4 s for a cutaway); land it on the word it illustrates.

## 6. Sound

- Dialogue first. Measure, do not guess: `ffmpeg -i out.mp4 -af ebur128=peak=true -f null -`. A common online delivery target is about -14 LUFS integrated with true peak at or below -1 dBTP (Spotify documents it; YouTube is widely reported near -14; TikTok and Meta publish no fixed number).
- Fill gaps with room tone, not digital silence.
- Music: chosen for this video's mood, about 12-18 dB under speech, up in speech-free moments, a breath of silence before the payoff. Licensed tracks only; note the source.
- Effects: few, on real events, quieter than the voice. No whoosh on every cut.

## 7. Picture

- Correct before styling: exposure, white balance, skin. Then one consistent look that matches the creator. No default teal-orange, no heavy LUT on faces.
- Hard cuts by default; a dissolve means time passed. No transition packs.
- Reframing for 9:16: check every shot, keep eyes in the upper third.

## 8. Honesty

Sole makes an edit feel crafted. It does not hide what is synthetic: realistic AI-generated people or events keep the platform's disclosure label, AI watermarks and content credentials are never removed, and no footage is made to look like a real testimonial or event that did not happen.

Credit: process, cut-edge and self-check rules adapted from video-use by Browser Use (MIT); pause trimming adapted from herk-edit-kit by Nate Herk (MIT). Modified.
