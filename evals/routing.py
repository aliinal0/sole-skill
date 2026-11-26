#!/usr/bin/env python3
"""Routing matrix: which Sole skill does each prompt open first? One short headless session per prompt, stopped at the
first Skill call, so it costs about $0.12 per prompt.

  python evals/routing.py                 # every prompt once
  python evals/routing.py --runs 3        # steadier
Results: evals/results/routing.json
"""
import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run  # noqa: E402

# expected: one skill, several acceptable ones joined by "|", or "none"
PROMPTS = [
    ("code", "Add a --json flag to cli.py that prints the report as JSON."),
    ("code", "Fix the bug where the cart total is wrong when the discount is 100%."),
    ("code", "Refactor utils.ts, it has three functions that do almost the same thing."),
    ("code", "Review my uncommitted changes before I push."),
    ("code", "Is there an SQL injection in db.py?"),
    ("code", "Which date library should I add to this Node project?"),
    ("code", "How is this codebase organised? I'm new here."),
    ("visual", "Design a settings screen for a habit tracker app."),
    ("visual", "Make the hero section bolder."),
    ("visual", "Write me a Midjourney prompt for a book cover."),
    ("visual", "Cut this interview transcript down to a 60-second short."),
    ("visual", "Does this video edit look AI-made? Notes are in edit.md."),
    ("write", "Rewrite this: 'We leverage cutting-edge synergies to empower teams.'"),
    ("write", "Write the release notes for version 2.3 from CHANGES.txt."),
    ("write", "What should the error message say when the upload is too big?"),
    ("write", "Draft a short email to my landlord about the broken heating."),
    ("business", "Write three Google ads for a dog-grooming salon."),
    ("business", "How should we price our new plan for small teams?"),
    ("business", "Why does our page not rank for 'vegan bakery leeds'?"),
    ("business", "Our trial-to-paid conversion is 3%. What should we test first?"),
    ("business", "Who are the main competitors of a browser-based invoicing app?"),
    ("sole", "Compare the three main password managers and give me sources."),
    ("sole", "Explain how OAuth works, I keep getting lost."),
    ("sole", "Remember that we deploy only on Tuesdays in this project."),
    ("sole", "You keep adding semicolons although I told you not to. Fix my setup."),
    ("sole", "Give me a product manager's view of this plan: launch in May with two features."),
    ("visual|write", "Build a landing page with copy for a pottery studio."),
    ("business|write", "Write ad copy for our coffee subscription that does not sound like AI."),
    ("none", "What is the capital of Portugal?"),
    ("none", "How do I undo my last git commit?"),
    ("none", "What does `chmod 644` mean? One line."),
    ("none", "Convert 5 miles to kilometres."),
    ("none", "Thanks, that worked!"),
    ("none", "What time zone is Istanbul in?"),
    ("none", "List the files in this folder."),
    ("none", "What does HTTP 404 mean? One sentence."),
    ("none", "Is 97 a prime number?"),
    ("none", "Which shell am I using?"),
]
OFF = json.dumps({"enabledPlugins": {"sole@sole-skill": False, "sole-browser@sole-skill": False}})


def first_skill(claude, prompt):
    with tempfile.TemporaryDirectory() as d:
        p = subprocess.run([claude, "-p", prompt, "--plugin-dir", run.ROOT, "--settings", OFF, "--strict-mcp-config",
                            "--tools", "Skill,Read,Glob,Grep", "--allowedTools", "Skill", "--max-turns", "2",
                            "--output-format", "stream-json", "--verbose"],
                           cwd=d, capture_output=True, text=True, encoding="utf-8", errors="replace")
    skills, cost, error = [], 0.0, None
    for line in p.stdout.splitlines():
        try:
            m = json.loads(line)
        except ValueError:
            continue
        if m.get("type") == "assistant":
            skills += [c["input"].get("skill", "") for c in m["message"]["content"]
                       if c.get("type") == "tool_use" and c.get("name") == "Skill"]
        if m.get("type") == "result":
            cost = m.get("total_cost_usd") or 0.0
            # running out of the two turns is expected after a Skill call; anything else is a failed session
            error = m.get("subtype") if m.get("is_error") and m.get("subtype") != "error_max_turns" else None
    if not p.stdout.strip():
        error = (p.stderr or "no output")[-200:]
    return [s.replace("sole:", "") for s in skills], cost, error


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--claude")
    a = ap.parse_args()
    sys.stdout.reconfigure(errors="replace")
    claude = run.find_claude(a.claude) or sys.exit("error: claude CLI not found")
    jobs = [(want, q) for want, q in PROMPTS for _ in range(a.runs)]
    with cf.ThreadPoolExecutor(4) as pool:
        got = list(pool.map(lambda j: first_skill(claude, j[1]), jobs))
    rows, good, bad, total = [], 0, 0, 0.0
    for (want, q), (skills, cost, error) in zip(jobs, got):
        total += cost
        ok = not error and ((not skills) if want == "none" else bool(skills) and skills[0] in want.split("|"))
        good, bad = good + ok, bad + bool(error)
        rows.append({"want": want, "prompt": q, "got": skills, "ok": ok, "error": error, "cost": cost})
        if not ok:
            print(f"{'ERROR' if error else 'MISS '} want {want:14} got {skills or 'none'}  {q}  {error or ''}")
    os.makedirs(run.RESULTS, exist_ok=True)
    with open(os.path.join(run.RESULTS, "routing.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=1)
    print(f"{good}/{len(jobs)} as expected, {bad} sessions failed, ${total:.2f}")
    sys.exit(0 if good == len(jobs) else 1)


if __name__ == "__main__":
    main()
