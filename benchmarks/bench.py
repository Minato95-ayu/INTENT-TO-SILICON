#!/usr/bin/env python3
import argparse, csv, os, statistics, subprocess, sys, tempfile, time

def run(cmd, reps):
    times, out = [], ""
    for _ in range(reps):
        t = time.perf_counter()
        r = subprocess.run(cmd, capture_output=True, text=True)
        times.append((time.perf_counter() - t) * 1000)
        out = r.stdout
        if r.returncode != 0:
            return None, f"exit {r.returncode}"
    return times, out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tezzc"); ap.add_argument("--aayu")
    ap.add_argument("--tezz-root", help="TezzNative repo root (where lib/ lives); default: guessed from --tezzc")
    ap.add_argument("--n", type=int, nargs="+", default=[1_000_000, 10_000_000])
    ap.add_argument("--reps", type=int, default=7)
    ap.add_argument("--csv", default="results.csv")
    a = ap.parse_args()
    tmp = tempfile.mkdtemp()
    if a.tezzc:
        a.tezzc = os.path.abspath(a.tezzc)
        a.tezz_root = a.tezz_root or os.path.dirname(os.path.dirname(os.path.dirname(a.tezzc)))
    rows = []

    for n in a.n:
        expect = str(n * (n - 1) // 2)
        impls = []

        # C (volatile so the loop cannot be optimised away)
        csrc = f"{tmp}/s.c"
        with open(csrc, "w") as f:
            f.write(
                f'#include <stdio.h>\nint main(){{volatile long long s=0;'
                f'for(long long i=0;i<{n}LL;i++)s+=i;printf("%lld\\n",s);return 0;}}'
            )
        for opt in ("-O0", "-O2"):
            exe = f"{tmp}/c{opt}.exe" if os.name == 'nt' else f"{tmp}/c{opt}"
            if subprocess.run(["gcc", opt, csrc, "-o", exe]).returncode == 0:
                impls.append((f"C {opt}", [exe], None))

        # TezzNative (native build) - Skip if not provided
        if a.tezzc:
            tn = f"{tmp}/s_{n}.tn"
            with open(tn, "w") as f:
                f.write(
                    f'import "std"\nfn main() -> int:\n  iters:int = {n}\n  i:int = 0\n'
                    f'  sum:int = 0\n  while i < iters:\n    sum = sum + i\n    i = i + 1\n'
                    f'  say sum\n  ret 0\n'
                )
            exe = f"{tmp}/tezz_{n}.exe" if os.name == 'nt' else f"{tmp}/tezz_{n}"
            r = subprocess.run([a.tezzc, "buildexe", tn, exe, "--target", "linux"],
                               capture_output=True, text=True, cwd=a.tezz_root)
            if r.returncode == 0:
                impls.append(("Tezz native", [exe], None))
            else:
                print("tezzc build failed:", r.stdout, r.stderr)

        # AAYU Rust VM (reports in-VM time too)
        if a.aayu:
            impls.append(("AAYU VM", [a.aayu, "--sum", str(n)], "AAYU_VM_NS"))

        # Python
        py = f"{tmp}/s.py"
        with open(py, "w") as f:
            f.write(
                f"i=0\ns=0\nwhile i<{n}:\n    s+=i\n    i+=1\nprint(s)\n"
            )
        impls.append(("Python", [sys.executable, py], None))

        for name, cmd, vm_tag in impls:
            times, out = run(cmd, a.reps)
            if times is None:
                rows.append((n, name, "FAILED", "", out)); continue
            lines = [l for l in out.strip().splitlines() if l.strip()]
            result = next((l for l in lines if l.strip().lstrip("-").isdigit()), "")
            ok = "OK" if result == expect else f"WRONG (got {result}, want {expect})"
            vm_ms = ""
            if vm_tag:
                for l in lines:
                    if l.startswith(vm_tag):
                        vm_ms = f"{int(l.split()[1]) / 1e6:.1f}"
            rows.append((n, name, f"{statistics.median(times):.1f}", vm_ms, ok))

    print(f"\n{'N':>12}  {'impl':12} {'proc ms (median)':>17} {'in-VM ms':>9}  result")
    for n, name, med, vm, ok in rows:
        print(f"{n:>12,}  {name:12} {med:>17} {vm:>9}  {ok}")
    
    with open(a.csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["N", "impl", "proc_ms_median", "in_vm_ms", "result"])
        w.writerows(rows)
    print(f"\nSaved {a.csv}. 'proc ms' includes process startup; one machine, small microbenchmark.")

if __name__ == "__main__":
    main()
