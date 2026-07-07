import os
import subprocess
import sys

def run_step(name, command):
    print(f"\n[{name}] Running: {command}")
    result = subprocess.run(command, shell=True, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if result.returncode != 0:
        print(f"âŒ {name} failed!")
        sys.exit(1)
    print(f"âœ… {name} passed!")

def main():
    print("ðŸš€ Running Local CI Pipeline...")
    
    # 1. Formatter Check (Mocked as a dry run)
    # Since aayu fmt formats in place, we just ensure it doesn't crash on standard files
    run_step("Formatter", "python tools/cli.py fmt tests/demo.aayu")
    
    # 2. Linter
    run_step("Linter", "python tools/cli.py lint tests/demo.aayu")
    
    # 3. Unit & Integration Tests
    run_step("Unit & Integration Tests", "python -m unittest discover -s tests")
    
    # 4. Build Packaging
    run_step("Build Packaging", "python scripts/package_release.py")
    
    print("\nðŸŽ‰ All CI Checks Passed Successfully!")

if __name__ == "__main__":
    main()

