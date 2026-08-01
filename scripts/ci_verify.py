import os
import sys
import subprocess
import datetime
import platform

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout

def main():
    log_path = "tests/conformance/ci_11B_verification.log"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=======================================\n")
        f.write(" AAYU CI Verification Report (Phase 11B)\n")
        f.write("=======================================\n\n")
        
        # 1. Timestamp
        f.write(f"Timestamp: {datetime.datetime.utcnow().isoformat()}Z\n")
        
        # 2. OS Info
        f.write(f"OS: {platform.system()} {platform.release()} ({platform.version()})\n")
        
        # 3. Compiler Info
        cl_output = run_cmd("cl")
        f.write(f"Compiler: {cl_output.splitlines()[0] if cl_output else 'MSVC Unknown'}\n")
        
        # 4. Commit Hash (mock for now since it's not a git repo yet, or we can check)
        git_hash = run_cmd("git rev-parse HEAD").strip()
        f.write(f"Commit Hash: {git_hash if 'fatal' not in git_hash else 'Development (Uncommitted)'}\n\n")
        
        f.write("=======================================\n")
        f.write(" 1. Building Runtime\n")
        f.write("=======================================\n")
        build_out = run_cmd("python build_runtime.py")
        f.write(build_out + "\n\n")
        
        f.write("=======================================\n")
        f.write(" 2. Running Conformance Suite\n")
        f.write("=======================================\n")
        test_out = run_cmd("python tests/conformance/test_runner.py")
        f.write(test_out + "\n\n")
        
        if "17 / 17 Features (100%)" in test_out:
            f.write("VERDICT: 17/17 PASS ✅\n")
            print("CI Verification completed successfully. 17/17 PASS.")
        else:
            f.write("VERDICT: FAILED ❌\n")
            print("CI Verification failed.")

if __name__ == "__main__":
    main()
