import os
import subprocess
import sys

def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode, result.stdout, result.stderr

def test_domain(intent_str):
    print(f"\n==============================================")
    print(f"Testing Intent: '{intent_str}'")
    print(f"==============================================")
    
    # 1. Build
    build_cmd = [sys.executable, "cli.py", "build", intent_str]
    code, out, err = run_cmd(build_cmd)
    
    if code != 0:
        print(f"[FAIL] Build failed for '{intent_str}'")
        print(err)
        return False
        
    print(out.strip())
    
    # Check if main.aayu exists
    if not os.path.exists("main.aayu"):
        print(f"[FAIL] main.aayu was not generated for '{intent_str}'")
        return False
        
    # 2. Compile
    compile_cmd = [sys.executable, "cli.py", "compile", "main.aayu"]
    code, out, err = run_cmd(compile_cmd)
    
    if code != 0:
        print(f"[FAIL] Compilation failed for '{intent_str}'")
        print(err)
        return False
        
    print(out.strip())
    print(f"[SUCCESS] {intent_str} verified successfully! SUCCESS")
    return True

if __name__ == "__main__":
    # Ensure we are in the prototype directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    intents = [
        "Build a CRM",
        "Build a Learning Management System",
        "Build an E-Commerce Platform",
        "Build a Hospital Management System",
        "Build an HRMS for employee leave and payroll"
    ]
    
    all_passed = True
    for intent in intents:
        if not test_domain(intent):
            all_passed = False
            
    if all_passed:
        print("\n\n[ALL SUCCESS] All 5 Domains Generated and Compiled Perfectly! SUCCESS")
    else:
        print("\n\n[FAIL] Some domains failed.")
