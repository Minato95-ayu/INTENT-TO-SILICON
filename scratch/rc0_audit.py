import subprocess
import time
import os
import shutil

# Setup a clean virtual environment
print("Setting up clean virtual environment...")
if os.path.exists("venv_audit"):
    shutil.rmtree("venv_audit")
subprocess.run("python -m venv venv_audit", shell=True)

# Use absolute paths for the executables to avoid relative path issues when changing directories
venv_path = os.path.abspath("venv_audit")
if os.name == 'nt':
    pip_cmd = os.path.join(venv_path, "Scripts", "pip.exe")
    aayu_cmd = os.path.join(venv_path, "Scripts", "aayu.exe")
else:
    pip_cmd = os.path.join(venv_path, "bin", "pip")
    aayu_cmd = os.path.join(venv_path, "bin", "aayu")

commands = [
    (f"{pip_cmd} install -e . --no-cache-dir", "."),
    (f"{aayu_cmd} --version", "."),
    (f"{aayu_cmd} doctor", "."),
    (f"{aayu_cmd} new DemoAppTest4", "."),
    (f"{aayu_cmd} run", "DemoAppTest4"),
    (f"{aayu_cmd} test", "DemoAppTest4"),
    (f"{aayu_cmd} format", "DemoAppTest4"),
    (f"{aayu_cmd} build", "DemoAppTest4"),
    (f"{aayu_cmd} build --target web", "DemoAppTest4"),
    (f"{aayu_cmd} benchmark", "DemoAppTest4")
]

report = "# RC0 Release Candidate Audit Report\\n\\n"
report += "This report was generated automatically on a clean virtual environment.\\n\\n"

for cmd, cwd in commands:
    report += f"## `{cmd}`\\n"
    start = time.time()
    try:
        if cwd != "." and not os.path.exists(cwd):
            os.makedirs(cwd, exist_ok=True)
        # We must use shell=False or provide full path. Since we have full path, we can just split the command string if it's simple.
        # But we will use shell=True and rely on the full path being quoted if necessary. It's safe here since no spaces in path.
        result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
        elapsed = time.time() - start
        status = "✅ PASS" if result.returncode == 0 else "❌ FAIL"
        
        report += f"**Status:** {status}\\n"
        report += f"**Execution Time:** {elapsed:.3f}s\\n"
        report += "### Console Output\\n"
        report += "```\\n"
        if result.stdout.strip():
            report += result.stdout.strip() + "\\n"
        if result.stderr.strip():
            report += result.stderr.strip() + "\\n"
        if not result.stdout.strip() and not result.stderr.strip():
            report += "<No output>\\n"
        report += "```\\n\\n"
        
    except Exception as e:
        elapsed = time.time() - start
        report += f"**Status:** ❌ ERROR\\n"
        report += f"**Execution Time:** {elapsed:.3f}s\\n"
        report += "### Exception\\n"
        report += "```\\n" + str(e) + "\\n```\\n\\n"

with open("RC0_REPORT.md", "w", encoding="utf-8") as f:
    f.write(report)

print("RC0_REPORT.md generated in clean venv.")
