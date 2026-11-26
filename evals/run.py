#!/usr/bin/env python3
"""Run Sole's test suite with one command, spending as few tokens as possible.

1. Free checks first (no tokens): plugin validation, script unit tests, module links, skill description
   length, grader regexes. If one fails, nothing is sent to Claude.
2. Eval cases (`claude plugin eval`), with and without the plugin, through a result cache:
   - a with-plugin result is reused until the case, the router/hooks/commands/agents, or a module the
     case uses changes;
   - a without-plugin (baseline) result is reused until the case itself changes, because the
     baseline never loads the plugin;
   - the model, effort level, judge model and CLI version are part of every cache key.
3. A Markdown report: evals/results/report.md (plus a dated copy).

  python evals/run.py                         # every case; only changed ones cost tokens
  python evals/run.py --case humanize-en ads-copy
  python evals/run.py --tag business
  python evals/run.py --effort medium         # sets CLAUDE_CODE_EFFORT_LEVEL for the runs
  python evals/run.py --runs 3                # 3 runs per arm, for steadier rates
  python evals/run.py --wait                  # on a usage limit, sleep until it resets and go on
  python evals/run.py --explain               # ask the judge why each failure failed (cached)
  python evals/run.py --static-only           # only the free checks
  python evals/run.py --report-only           # rebuild the report from the cache
  python evals/run.py --force                 # ignore the cache for the selected cases

Standard library only. Eval runs use your own Claude account and count toward its usage limits.
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVALS = os.path.join(ROOT, "evals")
SKILL = os.path.join(ROOT, "skills", "sole")
RESULTS = os.path.join(EVALS, "results")
CACHE = os.path.join(RESULTS, "cache")
CORE = ["skills/*/SKILL.md", ".claude-plugin/plugin.json", "hooks/*", "commands/*.md", "agents/*.md"]
LIMIT_RE = re.compile(r"hit your [^\n]*?limit[^\n]*?resets?\s+(?:at\s+)?(?:[a-z]{3,9}\.?\s+[0-9]{1,2},?\s+(?:at\s+)?)?([0-9]{1,2}(?::[0-9]{2})?\s*[ap]m|[0-9]{1,2}:[0-9]{2})", re.I)
PY_ONLY_RE = re.compile(r"\(\?(?:[aiLmsux]+\)|P[<=>])")
REF_RE = re.compile(r"`((?:core|build|business|research|write|templates|scripts)/[A-Za-z0-9/._-]+\.(?:md|py))`")
SHARED_RE = re.compile(r"^## Shared rules\n.*?(?=^## |\Z)", re.S | re.M)
STOP = threading.Event()


def log(msg):
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def sha(paths, extra=""):
    h = hashlib.sha256(extra.encode())
    for p in sorted(set(paths)):
        h.update(rel(p).encode())
        with open(p, "rb") as f:
            h.update(f.read())
    return h.hexdigest()[:16]


# ---------------------------------------------------------------- cases

def case_text(case):
    return open(os.path.join(EVALS, case, "case.yaml"), encoding="utf-8").read()


def list_cases(names, tags):
    found = {}
    for path in sorted(glob.glob(os.path.join(EVALS, "*", "case.yaml"))):
        name = os.path.basename(os.path.dirname(path))
        m = re.search(r"^tags:\s*\[(.*?)\]", open(path, encoding="utf-8").read(), re.M)
        found[name] = {t.strip() for t in m.group(1).split(",")} if m else set()
    if names:
        missing = [n for n in names if n not in found]
        if missing:
            sys.exit(f"error: unknown case(s): {', '.join(missing)}")
        return names
    return [n for n, t in found.items() if not tags or t & set(tags)]


def grader_blocks(case):
    body = case_text(case).split("\ngraders:", 1)[-1]
    out = []
    for b in re.split(r"\n  - type:", body)[1:]:
        name = re.search(r"^\s*name:\s*[\"']?([^\s\"']+)", b, re.M)
        crit = re.search(r"^( *)criteria:\s*[|>][-+]?\n((?:\1 +.*\n|\s*\n)+)", b + "\n", re.M)
        out.append({"type": b.split("\n", 1)[0].strip(), "name": name.group(1) if name else "", "body": b,
                    "with_only": bool(re.search(r"^\s*arm:\s*[\"']?with-only", b, re.M)),
                    "tool": (re.search(r"^\s*tool:\s*(\w+)", b, re.M) or [None, ""])[1],
                    "max": (re.search(r"^\s*max:\s*(\d+)", b, re.M) or [None, None])[1],
                    "input_match": (re.search(r"^\s*input_match:\s*'(.*)'\s*$", b, re.M) or [None, None])[1],
                    "pattern": pattern_of(b),
                    "criteria": textwrap.dedent(crit.group(2)).strip() if crit else None})
    return out


def pattern_of(block):
    """A grader's regex as YAML would read it: double-quoted values unescape \\\\ to \\."""
    m = re.search(r"^\s*pattern:\s*(\"(.*)\"|'(.*)')\s*$", block, re.M)
    if not m:
        return None
    return m.group(2).replace("\\\\", "\\").replace('\\"', '"') if m.group(2) is not None else m.group(3)


def with_only_graders(case):
    """Graders marked `arm: with-only` (plugin-fired indicators). If every grader is with-only, all are scored,
    the same rule the CLI uses."""
    blocks = grader_blocks(case)
    marked = {g["name"] for g in blocks if g["with_only"]}
    return set() if marked == {g["name"] for g in blocks} else marked


def module_files(case):
    """Skill files a case depends on: files its Read graders match, plus the files those modules point to."""
    all_files = [p for p in glob.glob(os.path.join(SKILL, "**", "*"), recursive=True) if os.path.isfile(p)]
    hits = set()
    for g in grader_blocks(case):
        pat = g["input_match"]
        if g["type"] != "tool_used" or g["tool"] != "Read" or g["max"] == "0" or not pat:
            continue
        try:
            rx = re.compile(pat)
        except re.error:
            rx = re.compile(re.escape(pat))
        for p in all_files:
            r = rel(p)
            if rx.search(r) or rx.search(r.replace("/", "\\")):
                hits.add(p)
    shared = SHARED_RE.search(open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8").read())
    hits |= {os.path.join(SKILL, r) for r in REF_RE.findall(shared.group(0) if shared else "")}
    todo = [p for p in hits if p.endswith(".md")]
    while todo:
        text = open(todo.pop(), encoding="utf-8").read()
        for ref in REF_RE.findall(text) + [f"scripts/{s}" for s in re.findall(r"scripts/([\w-]+\.py)", text)]:
            q = os.path.join(SKILL, ref)
            if os.path.isfile(q) and os.path.normpath(q) not in {os.path.normpath(h) for h in hits}:
                hits.add(q)
                if q.endswith(".md"):
                    todo.append(q)
    return {os.path.normpath(p) for p in hits}


def core_files():
    out = []
    for pat in CORE:
        out += [p for p in glob.glob(os.path.join(ROOT, pat)) if os.path.isfile(p)]
    return out


def case_files(case):
    return [p for p in glob.glob(os.path.join(EVALS, case, "**", "*"), recursive=True) if os.path.isfile(p)]


def keys(case, settings):
    base = sha(case_files(case), settings)
    return {"with": sha(case_files(case) + core_files() + list(module_files(case)), settings), "without": base}


def cache_path(case, arm, key):
    return os.path.join(CACHE, case, f"{arm}-{key}.json")


def cache_get(case, arm, key):
    p = cache_path(case, arm, key)
    if not os.path.isfile(p):
        return None
    data = json.load(open(p, encoding="utf-8"))
    runs = data.get("runs") or []
    bad = any(r.get("error") for r in runs) or "grader threw" in json.dumps(runs)
    return None if bad else data


def cache_put(case, arm, key, runs, meta):
    os.makedirs(os.path.join(CACHE, case), exist_ok=True)
    with open(cache_path(case, arm, key), "w", encoding="utf-8") as f:
        json.dump({"case": case, "arm": arm, "key": key, "meta": meta, "runs": runs}, f, indent=1)


# ---------------------------------------------------------------- free checks

def skill_checks():
    """Every Sole skill: a description of at most 1024 characters, a name that matches its folder, and the
    same Shared rules block as the general skill (so limits and economy rules cannot drift apart)."""
    problems, blocks = [], {}
    for path in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
        name = os.path.basename(os.path.dirname(path))
        text = open(path, encoding="utf-8").read()
        m = re.search(r"^description:\s*(.*)$", text, re.M)
        if not m or len(m.group(1)) > 1024:
            problems.append(f"{name}: description missing or over 1024 characters ({len(m.group(1)) if m else 0})")
        if not re.search(rf"^name:\s*{re.escape(name)}\s*$", text, re.M):
            problems.append(f"{name}: frontmatter name does not match its folder")
        b = SHARED_RE.search(text)
        blocks[name] = b.group(0).strip() if b else None
    ref = blocks.get("sole")
    for name, b in blocks.items():
        if b is None:
            problems.append(f"{name}: no '## Shared rules' block")
        elif ref and b != ref:
            problems.append(f"{name}: Shared rules block differs from skills/sole/SKILL.md")
    return problems


def static_checks(claude):
    problems = []
    proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=ROOT,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode:
        problems.append("unit tests failed:\n" + (proc.stderr or proc.stdout)[-2000:])
    if not claude:
        log("note: claude CLI not found, so `plugin validate` was skipped")
    for target in (".", "plugins/browser"):
        if claude and os.path.isdir(os.path.join(ROOT, target)):
            v = subprocess.run([claude, "plugin", "validate", target], cwd=ROOT, capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            if v.returncode:
                problems.append(f"plugin validate {target} failed:\n{(v.stdout + v.stderr)[-1500:]}")
    problems += skill_checks()
    for path in glob.glob(os.path.join(ROOT, "skills", "**", "*.md"), recursive=True) + \
            glob.glob(os.path.join(ROOT, "commands", "*.md")) + glob.glob(os.path.join(ROOT, "agents", "*.md")):
        if path.endswith("personas.md"):
            continue
        for ref in REF_RE.findall(open(path, encoding="utf-8").read()):
            if not os.path.isfile(os.path.join(SKILL, ref)):
                problems.append(f"{rel(path)} points to missing {ref}")
    for case in list_cases(None, None):
        for g in grader_blocks(case):
            if not g["name"] or ("input_match:" in g["body"] and not g["input_match"]):
                problems.append(f"{case}/{g['name'] or '?'}: grader needs a name, and input_match in single quotes")
            for field in ("input_match", "pattern"):
                if g[field] and PY_ONLY_RE.search(g[field]):
                    problems.append(f"{case}/{g['name']}: {field} uses Python-only syntax; the CLI runs JavaScript (use flags: i)")
                if g[field]:
                    try:
                        re.compile(g[field])
                    except re.error as e:
                        problems.append(f"{case}/{g['name']}: bad {field}: {e}")
        if not re.search(rf"^name:\s*{re.escape(case)}\s*$", case_text(case), re.M):
            problems.append(f"{case}: case name does not match its folder")
    return problems


# ---------------------------------------------------------------- running

def find_claude(explicit):
    for cand in (explicit, os.environ.get("CLAUDE_BIN"), shutil.which("claude")):
        if cand and (os.path.isfile(cand) or shutil.which(cand)):
            return cand
    # The Claude desktop app on Windows keeps its own CLI, newest version last, outside PATH.
    found = glob.glob(os.path.join(os.environ.get("LOCALAPPDATA", ""), "Claude-Data", "*", "claude-code", "*", "*", "claude.exe"))
    return max(found, key=os.path.getmtime) if found else None


def limit_reset(text):
    m = LIMIT_RE.search(text or "")
    return m.group(1) if m else None


def seconds_until(clock):
    clock = clock.replace(" ", "").lower()
    fmt = "%I:%M%p" if ":" in clock and clock[-2:] in ("am", "pm") else "%I%p" if clock[-2:] in ("am", "pm") else "%H:%M"
    t = dt.datetime.strptime(clock, fmt).time()
    now = dt.datetime.now()
    target = dt.datetime.combine(now.date(), t)
    if target <= now:
        target += dt.timedelta(days=1)
    return (target - now).total_seconds()


def run_case(claude, case, need, k, args, settings_meta):
    """need: 'both' or 'with'. Runs the CLI once and stores each arm in the cache."""
    if STOP.is_set():
        return case, "skipped"
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "result.json")
        cmd = [claude, "plugin", "eval", ROOT, "--case", case, "--scaffold", "--judge-model", args.judge_model,
               "--runs", str(args.runs), "-j", "2", "--trust-plugin", "--no-publish",
               "--allow-tools", "Write", "Edit", "WebFetch", "--json", out]
        if need == "with":
            cmd += ["--ablation", "none"]
        if args.model:
            cmd += ["--model", args.model]
        if args.max_cost:
            cmd += ["--max-cost-usd", str(args.max_cost)]
        env = dict(os.environ)
        if args.effort:
            env["CLAUDE_CODE_EFFORT_LEVEL"] = args.effort
        log(f"run  {case} ({'with Sole only' if need == 'with' else 'with and without'})")
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT, env=env)
        text = open(out, encoding="utf-8").read() if os.path.isfile(out) else ""
    cases_out = (json.loads(text).get("cases") or [{}]) if text else [{}]
    all_runs = [r for a in cases_out[0].get("arms", {}).values() for r in a or []]
    reset = limit_reset(proc.stdout + proc.stderr + " ".join(str(r.get("error") or "") for r in all_runs))
    if reset:
        STOP.set()
        log(f"limit {case}: usage limit hit, resets {reset}")
        return case, f"limit:{reset}"
    if not text:
        log(f"FAIL {case}: no result ({(proc.stdout + proc.stderr).strip()[-300:]})")
        return case, "error"
    failed = [r["error"] for r in all_runs if r.get("error")]
    for arm in ("with", "without"):
        runs = cases_out[0].get("arms", {}).get(arm)
        if runs and not any(r.get("error") for r in runs):
            cache_put(case, arm, k[arm], runs, settings_meta)
    if failed:
        log(f"FAIL {case}: {short(failed[0], 300)}")
        return case, "error"
    log(f"done {case}")
    return case, "ok"


# ---------------------------------------------------------------- explain

def explain(claude, case, runs, args):
    """Ask the judge, once, why each failed llm grader failed; stored inside the cached runs."""
    crit = {g["name"]: g["criteria"] for g in grader_blocks(case) if g["criteria"]}
    changed = False
    for r in runs:
        for g in r.get("graders", []):
            if g.get("passed") or g.get("why") or g["name"] not in crit or not g.get("evidence"):
                continue
            q = (f"You are grading the output of a coding agent against a criterion.\n\nCriterion:\n{crit[g['name']]}\n\n"
                 f"Agent output:\n{g['evidence']}\n\nIn at most 3 short lines, name only the parts of the criterion that "
                 "are not met and why. Then end with PASS or FAIL.")
            p = subprocess.run([claude, "-p", "--model", args.judge_model, "--max-turns", "1", "--output-format", "json"],
                               input=q, capture_output=True, text=True, encoding="utf-8", errors="replace")
            try:
                out = json.loads(p.stdout)
            except ValueError:
                continue
            why = (out.get("result") or "").strip()
            if p.returncode or out.get("is_error") or not why or LIMIT_RE.search(why):
                continue   # a refused or limited judge call is not an explanation; try again next time
            g["why"] = why
            changed = True
    return changed


def explain_all(claude, cases, settings, args):
    for case in cases:
        key = keys(case, settings)["with"]
        entry = cache_get(case, "with", key)
        if entry and explain(claude, case, entry["runs"], args):
            cache_put(case, "with", key, entry["runs"], entry.get("meta", {}))


# ---------------------------------------------------------------- report

def run_passed(r, skip):
    if r.get("error"):
        return False
    return all(g.get("passed") for g in r.get("graders", []) if g.get("name") not in skip)


def short(text, n):
    text = " ".join(str(text or "").split())
    return text if len(text) <= n else text[: n - 1] + "…"


def report(cases, settings, settings_label, static_problems):
    rows, details = [], []
    tot = {"with": [0, 0], "without": [0, 0]}
    cost = {"with": 0.0, "without": 0.0}
    turns = {"with": 0, "without": 0}
    missing, both = [], {"with": [0, 0], "without": [0, 0]}
    for case in cases:
        k = keys(case, settings)
        skip = with_only_graders(case)
        cells, seen = [], {}
        for arm in ("with", "without"):
            entry = cache_get(case, arm, k[arm])
            if not entry:
                cells.append(("-", ""))
                if arm == "with":
                    missing.append(case)
                continue
            runs = entry["runs"]
            ok = sum(1 for r in runs if run_passed(r, skip))
            tot[arm][0] += ok
            tot[arm][1] += len(runs)
            seen[arm] = (ok, len(runs))
            cost[arm] += sum((r.get("costUsd") or 0) + (r.get("judgeCostUsd") or 0) for r in runs)
            turns[arm] += sum(r.get("turns") or 0 for r in runs)
            fails = sorted({g["name"] for r in runs for g in r.get("graders", []) if not g.get("passed")})
            cells.append((f"{ok}/{len(runs)}", ", ".join(fails)))
            for r in runs:
                for g in r.get("graders", []):
                    if not g.get("passed"):
                        details.append((case, arm, g))
        if len(seen) == 2:
            for arm, (ok, n) in seen.items():
                both[arm][0] += ok
                both[arm][1] += n
        rows.append(f"| {case} | {cells[0][0]} | {short(cells[0][1], 60)} | {cells[1][0]} | {short(cells[1][1], 60)} |")

    def per_pass(arm):
        return f"${cost[arm] / tot[arm][0]:.3f}" if tot[arm][0] else "-"

    lines = [f"# Sole test report - {dt.datetime.now():%Y-%m-%d %H:%M}", "", f"Settings: {settings_label}", ""]
    lines += ["Free checks: " + ("not run" if static_problems is None else "FAIL" if static_problems else "pass"), ""]
    lines += [f"Eval runs passed: with Sole {tot['with'][0]}/{tot['with'][1]}, without {tot['without'][0]}/{tot['without'][1]}.",
              f"Cost (agent + judge): with ${cost['with']:.2f}, without ${cost['without']:.2f}; per passing answer "
              f"{per_pass('with')} vs {per_pass('without')}. Turns: {turns['with']} vs {turns['without']}.", ""]
    if both["with"][1] and both["with"][1] != tot["with"][1]:
        lines += [f"Over the cases that have both arms: with Sole {both['with'][0]}/{both['with'][1]}, "
                  f"without {both['without'][0]}/{both['without'][1]}.", ""]
    commands = [c for c in cases if re.search(r"prompt: \|\n\s+/sole:", case_text(c))]
    if commands:
        lines += [f"Slash-command cases (plain Claude cannot pass these by construction): {', '.join(commands)}", ""]
    if missing:
        lines += [f"No with-Sole result yet for: {', '.join(missing)}", ""]
    lines += ["Graders marked with-only (did the plugin load, was the module read) are listed when they fail but only "
              "decide pass or fail when every grader of a case is with-only.", "",
              "| Case | With Sole | Failed graders | Without | Failed graders |", "|---|---|---|---|---|", *rows, ""]
    if details:
        lines += ["## Failures", ""]
        for case, arm, g in details:
            lines.append(f"- **{case}** ({arm}) `{g.get('name')}`: {short(g.get('explanation'), 160)}")
            if g.get("why"):
                lines.append(f"  - judge: {short(g['why'], 400)}")
            elif g.get("evidence"):
                lines.append(f"  - answer starts: {short(g['evidence'], 300)}")
        lines.append("")
    if static_problems:
        lines += ["## Free check problems", "", *[f"- {short(p, 500)}" for p in static_problems], ""]
    os.makedirs(RESULTS, exist_ok=True)
    text = "\n".join(lines)
    path = os.path.join(RESULTS, "report.md")
    for p in (path, os.path.join(RESULTS, f"report-{dt.datetime.now():%Y%m%d-%H%M}.md")):
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
    return path, tot, missing


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--case", nargs="+", help="case names (folder names in evals/)")
    ap.add_argument("--tag", nargs="+", help="run cases that have any of these tags")
    ap.add_argument("--parallel", type=int, default=2, help="cases at once (default 2)")
    ap.add_argument("--runs", type=int, default=1, help="runs per arm (default 1)")
    ap.add_argument("--model", help="model for the agent runs (default: the CLI's)")
    ap.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"], help="effort level for the agent runs")
    ap.add_argument("--judge-model", default="sonnet")
    ap.add_argument("--max-cost", type=float, default=3.0, help="cost ceiling per case in USD (default 3)")
    ap.add_argument("--with-only", action="store_true", help="never run the baseline; use cached baselines only")
    ap.add_argument("--force", action="store_true", help="ignore cached results for the selected cases")
    ap.add_argument("--wait", action="store_true", help="on a usage limit, sleep until reset and continue")
    ap.add_argument("--explain", action="store_true", help="ask the judge why each failure failed (costs a little)")
    ap.add_argument("--static-only", action="store_true", help="run only the free checks")
    ap.add_argument("--no-static", action="store_true", help="skip the free checks")
    ap.add_argument("--report-only", action="store_true", help="only rebuild the report from the cache")
    ap.add_argument("--claude", help="path to the claude CLI")
    args = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(errors="replace")

    claude = find_claude(args.claude)
    cases = list_cases(args.case, args.tag)
    version = ""
    if claude:
        version = subprocess.run([claude, "--version"], capture_output=True, text=True).stdout.strip()
    settings = f"model={args.model or 'default'}|effort={args.effort or os.environ.get('CLAUDE_CODE_EFFORT_LEVEL') or 'default'}|judge={args.judge_model}|runs={args.runs}|cli={version}"
    label = settings.replace("|", ", ")

    problems = [] if args.no_static or args.report_only else static_checks(claude)
    if problems:
        log("free checks failed; no tokens spent:")
        for p in problems:
            print("  - " + p.replace("\n", "\n    "))
    else:
        log("free checks: ok" if not (args.no_static or args.report_only) else "free checks: skipped")
    if args.static_only or args.report_only or problems:
        if args.report_only:
            if args.explain and claude:
                explain_all(claude, cases, settings, args)
            log(f"report: {report(cases, settings, label, None)[0]}")
        sys.exit(1 if problems else 0)
    if not claude:
        sys.exit("error: claude CLI not found. Pass --claude PATH or set CLAUDE_BIN.")

    meta = {"settings": settings, "at": dt.datetime.now().isoformat(timespec="seconds")}
    while True:
        todo = []
        for case in cases:
            k = keys(case, settings)
            have_with = not args.force and cache_get(case, "with", k["with"])
            have_without = not args.force and cache_get(case, "without", k["without"])
            if have_with and (have_without or args.with_only):
                continue
            todo.append((case, "with" if (have_without or args.with_only) else "both", k))
        if not todo:
            break
        log(f"{len(todo)} of {len(cases)} cases need a run; the rest come from the cache")
        STOP.clear()
        resets = []
        with cf.ThreadPoolExecutor(max_workers=max(1, args.parallel)) as pool:
            for case, status in pool.map(lambda t: run_case(claude, t[0], t[1], t[2], args, meta), todo):
                if status.startswith("limit:"):
                    resets.append(status.split(":", 1)[1])
        args.force = False   # forced cases ran once; do not loop on them
        if not resets:
            break
        if not args.wait:
            log(f"stopped at the usage limit (resets {resets[0]}). Run the same command again to resume.")
            break
        wait = seconds_until(resets[0]) + 120
        log(f"waiting {wait / 60:.0f} min for the limit to reset ({resets[0]})")
        time.sleep(wait)

    if args.explain:
        explain_all(claude, cases, settings, args)

    path, tot, missing = report(cases, settings, label, None if args.no_static else [])
    log(f"report: {path}")
    log(f"with Sole {tot['with'][0]}/{tot['with'][1]}, without {tot['without'][0]}/{tot['without'][1]}")
    sys.exit(0 if tot["with"][1] and not missing and tot["with"][0] == tot["with"][1] else 1)


if __name__ == "__main__":
    main()
