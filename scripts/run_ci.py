import os
import subprocess
import sys
import tempfile
import shutil

def run_step(name, command, cwd=None):
    print(f"\n[{name}] Running: {command}")
    result = subprocess.run(command, shell=True, env=dict(os.environ, PYTHONIOENCODING="utf-8"), cwd=cwd)
    if result.returncode != 0:
        print(f"[FAIL] {name} failed!")
        sys.exit(1)
    print(f"[PASS] {name} passed!")

def main():
    print("Running Local CI Pipeline...")
    
    # 0. System Packaging & CLI E2E Check
    run_step("Packaging (Install)", "pip install -e .")
    run_step("CLI Global Check", "aayu --version")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        run_step("CLI Init", "aayu init ci_demo", cwd=temp_dir)
        demo_dir = os.path.join(temp_dir, "ci_demo")
        os.makedirs(os.path.join(demo_dir, "src"), exist_ok=True)
        with open(os.path.join(demo_dir, "src", "main.aayu"), "w", encoding="utf-8") as f:
            f.write("print(\"CI Pass\").\n")
        run_step("CLI Build", "aayu build", cwd=demo_dir)
        run_step("CLI Run", "aayu run", cwd=demo_dir)

    # 1. Formatter Check
    run_step("Formatter", "aayu fmt tests/demo.aayu")
    
    # 2. Linter
    run_step("Linter", "aayu lint tests/demo.aayu")
    
    # 3. Unit & Integration Tests
    run_step("Unit & Integration Tests", "python -m unittest discover -s tests")
    
    # 4. Build Packaging
    run_step("Build Packaging", "python scripts/package_release.py")
    
    print("\nAll CI Checks Passed Successfully!")

if __name__ == "__main__":
    main()

