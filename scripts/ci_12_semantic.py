import os
import sys
import datetime
import platform
import subprocess

def run_ci():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    log_dir = os.path.join(repo_root, "tests", "conformance")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "semantic_pipeline_ci.log")

    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
    
    print("Running Phase 12.0 Semantic Verification CI...")
    
    # Run pytest
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/compiler/test_semantic_12.py", "-v"],
        cwd=repo_root,
        capture_output=True,
        text=True
    )
    
    passed = result.returncode == 0
    verdict = "PASS \u2705" if passed else "FAIL \u274c"
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("=======================================\n")
        f.write(" AAYU CI Verification Report (Phase 12.0)\n")
        f.write("=======================================\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"OS: {os_info}\n\n")
        f.write(result.stdout)
        f.write("\n")
        if result.stderr:
            f.write("--- STDERR ---\n")
            f.write(result.stderr)
            f.write("\n")
        f.write(f"VERDICT: {verdict}\n")
        
    print(f"CI Log saved to: {log_file}")
    if not passed:
        print("Tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    run_ci()
