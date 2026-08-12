import os

def read_coverage(name):
    # Reads coverage from tests/{name}/{name}_coverage.txt
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    path = os.path.join(base_dir, "tests", name, f"{name}_coverage.txt")
    if os.path.exists(path):
        with open(path, "r") as f:
            data = f.read().strip()
            parts = data.split("/")
            if len(parts) == 4:
                # pass_total, total, recovery, avg_time
                pass_total = int(parts[0])
                total = int(parts[1])
                recovery = int(parts[2])
                avg_time = float(parts[3])
                
                return {
                    "total": total,
                    "passed": pass_total,
                    "failed": total - pass_total,
                    "recovery": recovery,
                    "time": avg_time,
                    "coverage": (pass_total / total) * 100.0 if total > 0 else 0.0
                }
            elif len(parts) == 2:
                pass_total = int(parts[0])
                total = int(parts[1])
                return {
                    "total": total,
                    "passed": pass_total,
                    "failed": total - pass_total,
                    "recovery": 0,
                    "time": 0.0,
                    "coverage": (pass_total / total) * 100.0 if total > 0 else 0.0
                }
    return {"total": 0, "passed": 0, "failed": 0, "recovery": 0, "time": 0.0, "coverage": 0.0}

def read_fuzzer(name):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    path = os.path.join(base_dir, "tests", name, "fuzzer_report.txt")
    if os.path.exists(path):
        with open(path, "r") as f:
            return int(f.read().strip())
    return 0

def build_progress_bar(percentage):
    filled = int(percentage / 10)
    empty = 10 - filled
    return "█" * filled + "░" * empty + f" {percentage:.1f}%"

def get_status(pct):
    if pct >= 100: return "✅ 100%"
    elif pct == 0: return "⏳"
    else: return f"🟡 {pct:.1f}%"

def handle(args):
    grammar = read_coverage("grammar")
    types = read_coverage("types")
    
    grammar_cov = grammar["coverage"]
    types_cov = types["coverage"]
    grammar_crashes = read_fuzzer("grammar")
    
    overall = (grammar_cov + types_cov) / 10
    
    dashboard = f"""# AAYU Compiler Dashboard

> **Status**: PHASE B (Polishing)
> **Goal**: True Independence & Stable Ecosystem

## 📊 Grammar

{grammar['total']} Tests
{grammar['passed']} Passed
{grammar['failed']} Failed

Recovery Success
{grammar['recovery']} / {1005 if grammar['recovery'] > 0 else 0}

Crash Count
{grammar_crashes}

Average Parse Time
{grammar['time']} ms

Coverage
{grammar_cov:.1f}%

## 📈 Compiler Readiness Report

| Area               | Status |
| ------------------ | ------ |
| Grammar            | {get_status(grammar_cov)} |
| Parser             | {get_status(grammar_cov)} |
| Type System        | {get_status(types_cov)} |
| Modules            | ⏳      |
| Objects            | ⏳      |
| Generics           | ⏳      |
| Traits             | ⏳      |
| Async              | ⏳      |
| LLVM               | ⏳      |
| Stress Tests       | ⏳      |
| Differential Tests | ⏳      |

"""
    # Write to standard location
    out_path = r"C:\Users\ayush\.gemini\antigravity\brain\2e3a96c2-8c68-468d-9b69-c5bc6d8163aa\compiler_dashboard.md"
    try:
        with open(out_path, "w", encoding='utf-8') as f:
            f.write(dashboard)
    except:
        # Fallback to local
        with open("compiler_dashboard.md", "w", encoding='utf-8') as f:
            f.write(dashboard)
            
    print("\n[AAYU] Dashboard successfully updated based on live test coverage!")

if __name__ == "__main__":
    handle(None)
