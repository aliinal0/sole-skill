#!/usr/bin/env bash
cat > edl.json <<'JSON'
[
 {
  "source": "talk.mp4",
  "start": 0.4,
  "end": 1.9,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 2.02,
  "end": 3.52,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 3.64,
  "end": 5.14,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 5.26,
  "end": 6.76,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 6.88,
  "end": 8.38,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 8.5,
  "end": 10.0,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 10.12,
  "end": 11.62,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 11.74,
  "end": 13.24,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 13.36,
  "end": 14.86,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 14.98,
  "end": 16.48,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 16.6,
  "end": 18.1,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 18.22,
  "end": 19.72,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 19.84,
  "end": 21.34,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 21.46,
  "end": 22.96,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 23.08,
  "end": 24.58,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 24.7,
  "end": 26.2,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 26.32,
  "end": 27.82,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 27.94,
  "end": 29.44,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 29.56,
  "end": 31.06,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 31.18,
  "end": 32.68,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 32.8,
  "end": 34.3,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 34.42,
  "end": 35.92,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 36.04,
  "end": 37.54,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 },
 {
  "source": "talk.mp4",
  "start": 37.66,
  "end": 39.16,
  "zoom": "punch-in 120%",
  "sfx": "whoosh"
 }
]
JSON
cat > edit_notes.md <<'MD'
# Edit notes - "My first month freelancing" (YouTube, 16:9)

- Silence remover at -30 dB, minimum 0.1 s: every pause removed.
- Cut every 1.5 s exactly to keep retention high (see edl.json).
- Punch-in zoom to 120% on every cut, whoosh sound effect on every cut.
- Captions: one word at a time, bold yellow uppercase, emoji after key words (money -> 💰, late -> ⏰).
- B-roll: stock clip for every sentence (laptop typing, cash counting, calendar flipping, handshake).
- Music: upbeat royalty-free track at -6 dB under the voice for the whole video, no changes.
- Grade: teal-orange cinematic LUT at 100% on everything.
- Hook text on screen at 0 s: "What if I told you freelancing is a trap?"
MD
