# Video tells - what makes an edit look automatic

Each row is a default, not a ban. It is right when the creator's style (`.claude/EDITSTYLE.md`) or the user's request chose it. It is a tell when it arrived because nothing was decided.

## Real footage

| Tell | A person would | Right when |
|---|---|---|
| Every pause removed; speech runs breathless | Shrink long pauses, keep a breath, keep the pause before a point | Fast ad cut on request |
| Shots of near-equal length, cut like a metronome | Let length follow the content: hold on proof, emotion, laughs | Music video cut to a beat on purpose |
| A zoom punch-in on every sentence or cut | Change framing only to hide a jump or mark one moment | The creator's own established style |
| Word-by-word captions, bouncing, uppercase, emoji, colour on every keyword | Phrase-level, sentence-case captions timed to speech | Short-form for a creator who already uses that look |
| A whoosh, riser or swipe on every cut | Hard cuts; a sound only on a real event | One designed transition in the whole video |
| Stock B-roll for every noun ("money" -> cash, "growth" -> chart) | Own footage where it shows something; otherwise stay on the speaker | A list the speaker is literally reading |
| One music bed at one level from start to end | Music that rises in speech-free moments, dips under speech, stops before the payoff | Background music for a long livestream |
| Default teal-orange grade or a strong LUT on faces | Correct first, then one look that suits the creator and skin | The brand's documented look |
| Generic hook lines ("What if I told you...", "Here's the thing", "Stop scrolling") | Open on the most specific moment from the footage | Never by default |
| Every retake, laugh and aside cut, so the person sounds scripted | Keep the laughs, jokes and asides that are the creator's voice | A formal corporate piece on request |
| Long dead air or a frozen frame left in | Trim or cover it | A designed held beat with a reason |
| AI voice-over over real footage without the user asking | The creator's own voice | User chose a synthetic voice and it is disclosed |

## Motion graphics and promos

Use the "Never ship" list in `build/video/motion.md`: corner labels and counters, slide-deck layouts, invented stats, slogan copy ("Not just X. It's Y."), a small card on an empty background, an end card held past ~1.4 s, effects used to show effort.

## Measured checks (`scripts/video_check.py`)

| Check | Flag | Why it matters |
|---|---|---|
| Shot-length variation (CV of shot lengths) | Below 0.35 with 8+ shots (soft note below 0.6 when over 20% of shots sit near the median) | Even rhythm reads as automated. In 40 human-edited films (public CC BY shot data, Keaton and early Hitchcock) CV ran 0.72-1.95 |
| Share of shots within ±15% of the median | Above 60% (soft note above 30%) | Same signal, steadier on short videos; the films ran 8-20% |
| Pause share in speech | Below ~2% over 60+ s | Breathless, every pause removed |
| Longest silence | Above ~2.5 s | Dead air |
| Integrated loudness, true peak | Far from about -14 LUFS, true peak above -1 dBTP | Too quiet, or clipping after platform normalisation |

Thresholds are starting heuristics, not standards: film is not vlog editing, and no measured data for vlogs exists yet. Report the numbers and judge them against the creator's style. Cut detection finds hard cuts and most jump cuts (it looks for score spikes against neighbouring frames), but shaky handheld footage can add a false cut or two; a cut list (`--edl`) is always more exact.

## Review order

1. Watch the first 5 seconds and the last 5 seconds.
2. Look at the frames around every cut and listen to every join.
3. Run the measured checks.
4. Go down the tables above; note each tell with its timestamp and the fix.
5. Quote only what is in the footage, transcript or notes you were given. Do not invent lines, moments, numbers or reactions to illustrate a fix; if an example helps, write a neutral one ("a line you want to land") or say what you would need to see.
6. Reviewing only a plan or cut list, without the footage: report what the files show as fact, and what they only suggest as a risk to check ("cuts on a fixed timer are likely to land mid-word; listen to each join"), never as something you heard or saw.

Credit: motion-graphics list condensed from motionmaxxing by Tejashmakwana (Apache-2.0); real-footage list informed by video-use by Browser Use (MIT) and herk-edit-kit by Nate Herk (MIT). Modified.
