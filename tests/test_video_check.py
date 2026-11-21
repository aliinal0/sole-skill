"""Tests for skills/sole/scripts/video_check.py (cut-list mode and the scoring rules; no ffmpeg needed)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
SCRIPT = os.path.join(HERE, "..", "skills", "sole", "scripts", "video_check.py")
sys.path.insert(0, os.path.dirname(SCRIPT))
import video_check as vc  # noqa: E402

# Shot lengths in the range a person might cut a talking-head video (seconds).
VARIED = [2.1, 6.8, 1.2, 4.4, 11.5, 3.0, 0.9, 7.6, 2.6, 5.2, 1.7, 9.3]


def edl(lengths, gap=0.0, key=("start", "end")):
    t, rows = 0.0, []
    for x in lengths:
        rows.append({key[0]: round(t, 3), key[1]: round(t + x, 3)})
        t += x + gap
    return rows


class RhythmTests(unittest.TestCase):
    def test_metronome_cuts_are_flagged(self):
        r = vc.rhythm([1.5] * 24)
        self.assertEqual(r["cv"], 0.0)
        self.assertEqual(r["even_share"], 1.0)
        flags, _ = vc.findings(r, 36, None, None, None)
        self.assertTrue(any(f.startswith("even rhythm") for f in flags))

    def test_varied_cuts_are_not_flagged(self):
        r = vc.rhythm(VARIED)
        self.assertGreater(r["cv"], 0.6)
        flags, notes = vc.findings(r, sum(VARIED), None, None, None)
        self.assertEqual(flags, [])
        self.assertFalse(any("rhythm" in n for n in notes))

    def test_few_shots_are_not_judged(self):
        flags, notes = vc.findings(vc.rhythm([1.5] * 5), 7.5, None, None, None)
        self.assertEqual(flags + notes, [])

    def test_tiny_fragments_are_ignored(self):
        self.assertEqual(vc.rhythm([0.01, 0.02, 3.0, 4.0])["shots"], 2)


class AudioRuleTests(unittest.TestCase):
    def test_breathless_and_dead_air(self):
        flags, _ = vc.findings({"shots": 1}, 120, [0.3, 0.4], None, None)
        self.assertTrue(any(f.startswith("breathless") for f in flags))
        flags, _ = vc.findings({"shots": 1}, 120, [1.0, 3.2, 2.0], None, None)
        self.assertTrue(any(f.startswith("dead air") for f in flags))

    def test_short_clip_is_not_called_breathless(self):
        flags, _ = vc.findings({"shots": 1}, 40, [0.2], None, None)
        self.assertFalse(any(f.startswith("breathless") for f in flags))

    def test_loudness_and_true_peak(self):
        flags, notes = vc.findings({"shots": 1}, 60, None, -22.0, -0.4)
        self.assertTrue(any("true peak" in f for f in flags))
        self.assertTrue(any("loudness" in n for n in notes))
        flags, notes = vc.findings({"shots": 1}, 60, None, -14.0, -1.5)
        self.assertEqual(flags + notes, [])


class CliTests(unittest.TestCase):
    def run_cli(self, rows):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "edl.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(rows, f)
            out = subprocess.run([sys.executable, SCRIPT, "--edl", path, "--json"],
                                 capture_output=True, text=True, check=True).stdout
        return json.loads(out)

    def test_edl_list_with_gaps(self):
        report = self.run_cli(edl([1.5] * 24, gap=0.12))
        self.assertEqual(report["rhythm"]["shots"], 24)
        self.assertAlmostEqual(report["duration_s"], 36.0, places=1)
        self.assertTrue(any(f.startswith("even rhythm") for f in report["flags"]))
        self.assertIsNone(report["pause_share"])

    def test_edl_segments_dict_with_in_out_keys(self):
        report = self.run_cli({"segments": edl(VARIED, key=("in", "out"))})
        self.assertEqual(report["rhythm"]["shots"], len(VARIED))
        self.assertEqual(report["flags"], [])

    def test_no_input_is_an_error(self):
        res = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)


if __name__ == "__main__":
    unittest.main()
