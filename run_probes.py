#!/usr/bin/env python3
"""
AAYU probe runner (cross-platform, no dependencies beyond the repo itself).

Usage (from anywhere):
    python run_probes.py --repo /path/to/INTENT-TO-SILICON            # everything
    python run_probes.py --repo . --only probes                       # just the 12 probes
    python run_probes.py --repo . --skip-web                          # no HTTP checks

What it checks (a test only passes if the OUTPUT is right, not merely "no error"):
  1. probes     : each probes/NN_name.aayu is run; every line of NN_name.expected must
                  appear in stdout, in order. Forbidden markers fail the probe.
  2. handbook   : every ```aayu block in AAYU_LANGUAGE_HANDBOOK_V1.md must compile
                  without an error marker (docs must not lie).
  3. examples   : every .aayu under examples/ and repo root must run without markers.
  4. new        : `aayu new` project must run.
  5. web        : aayugram.aayu --web: GET / == 200 and GET /api/feed == 200 on same port.

Exit code 0 only if everything passes.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Any of these in output means failure, even if the process exit code is 0.
FORBIDDEN = [
    "Error:", "Runtime Error", "Traceback", "VM CRASH", "Semantic Error",
    "VM Warning", "Unresolved native function", "Unexpected character",
]
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def run_aayu(repo, args, cwd, timeout=30):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONIOENCODING"] = "utf-8"
    cmd = [sys.executable, "-m", "tools.cli"] + args
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, ANSI.sub("", p.stdout + "\n" + p.stderr)
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") if isinstance(e.stdout, str) else ""
        return 124, "TIMEOUT\n" + out


def bad_markers(out):
    return [m for m in FORBIDDEN if m in out]


def ordered_contains(out_lines, expected):
    """expected lines must appear in order (other lines in between are allowed)."""
    i = 0
    for line in out_lines:
        if i < len(expected) and line.strip() == expected[i].strip():
            i += 1
    return i == len(expected), (expected[i] if i < len(expected) else None)


class Report:
    def __init__(self):
        self.rows = []

    def add(self, group, name, ok, detail=""):
        self.rows.append((group, name, ok, detail))
        print(f"{'PASS' if ok else 'FAIL'}  [{group}] {name}" + (f"  -> {detail}" if detail and not ok else ""))

    def summary(self):
        groups = {}
        for g, _, ok, _ in self.rows:
            a = groups.setdefault(g, [0, 0])
            a[1] += 1
            a[0] += 1 if ok else 0
        print("\n===== SUMMARY =====")
        for g, (p, t) in groups.items():
            print(f"{g:10s} {p}/{t}")
        tp = sum(1 for r in self.rows if r[2])
        print(f"{'TOTAL':10s} {tp}/{len(self.rows)}")
        return tp == len(self.rows)


def probes(repo, rep):
    for src in sorted((HERE / "probes").glob("*.aayu")):
        exp_file = src.with_suffix(".expected")
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copy(src, tmp)
            rc, out = run_aayu(repo, ["run", "--console", src.name], tmp)
            bad = bad_markers(out)
            exp = exp_file.read_text(encoding="utf-8").splitlines() if exp_file.exists() else []
            ok_order, missing = ordered_contains(out.splitlines(), exp)
            if bad:
                rep.add("probes", src.name, False, "marker: " + ", ".join(bad))
            elif not ok_order:
                rep.add("probes", src.name, False, f"expected line not found: {missing!r}")
            else:
                rep.add("probes", src.name, True)


def handbook(repo, rep):
    hb = repo / "AAYU_LANGUAGE_HANDBOOK_V1.md"
    if not hb.exists():
        rep.add("handbook", "file exists", False, "AAYU_LANGUAGE_HANDBOOK_V1.md missing")
        return
    blocks = re.findall(r"```aayu\n(.*?)```", hb.read_text(encoding="utf-8"), flags=re.S)
    for i, code in enumerate(blocks, 1):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / f"hb_block_{i}.aayu"
            f.write_text(code, encoding="utf-8")
            rc, out = run_aayu(repo, ["run", "--console", f.name], tmp, timeout=30)
            bad = bad_markers(out)
            first = next((l for l in out.splitlines() if any(m in l for m in FORBIDDEN)), "")
            rep.add("handbook", f"block #{i} ({code.strip().splitlines()[0][:30] if code.strip() else 'empty'})",
                    not bad, first[:110])


def examples(repo, rep):
    files = sorted([f for f in set(list(repo.glob("*.aayu")) + list(repo.glob("examples/**/*.aayu"))) if f.is_file()])
    for f in files:
        rel = f.relative_to(repo)
        with tempfile.TemporaryDirectory() as tmp:
            rc, out = run_aayu(repo, ["run", "--console", str(f)], tmp, timeout=30)
            bad = bad_markers(out)
            first = next((l for l in out.splitlines() if any(m in l for m in FORBIDDEN)), "")
            rep.add("examples", str(rel).replace("\\", "/"), rc != 124 and not bad, first[:110])


def new_project(repo, rep):
    with tempfile.TemporaryDirectory() as tmp:
        rc, out = run_aayu(repo, ["new", "probe_proj"], tmp)
        proj = Path(tmp) / "probe_proj"
        if not proj.exists():
            rep.add("new", "aayu new creates project", False, out[-120:])
            return
        rc, out = run_aayu(repo, ["run", "--console"], str(proj))
        rep.add("new", "aayu new + aayu run", not bad_markers(out), out.strip().splitlines()[-1][:110] if out.strip() else "")


def http_get(url, timeout=4):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def web(repo, rep, port=3199):
    app = repo / "aayugram.aayu"
    if not app.exists():
        rep.add("web", "aayugram.aayu exists", False)
        return
    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo) + os.pathsep + env.get("PYTHONPATH", "")
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.Popen([sys.executable, "-m", "tools.cli", "run", str(app), "--web", f"--port={port}"],
                                cwd=tmp, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            time.sleep(8)
            rep.add("web", f"GET / on :{port}", http_get(f"http://127.0.0.1:{port}/") == 200)
            code = http_get(f"http://127.0.0.1:{port}/api/feed")
            rep.add("web", f"GET /api/feed on same port :{port}", code == 200, f"got {code}")
        finally:
            proc.kill()
            proc.wait()
            time.sleep(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--only", choices=["probes", "handbook", "examples", "new", "web"])
    ap.add_argument("--skip-web", action="store_true")
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    rep = Report()
    steps = {"probes": probes, "handbook": handbook, "examples": examples, "new": new_project, "web": web}
    for name, fn in steps.items():
        if a.only and a.only != name:
            continue
        if name == "web" and a.skip_web:
            continue
        fn(repo, rep)
    sys.exit(0 if rep.summary() else 1)


if __name__ == "__main__":
    main()

