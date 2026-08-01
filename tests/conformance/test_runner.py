import os
import subprocess
import sys
import glob
import tempfile

# Test suite expected outputs
EXPECTED = {
    "001_print.aayu": "Hello, Native AAYU!",
    "002_variables.aayu": "30",
    "003_arithmetic.aayu": "50\n60\n20\n50",
    "004_boolean.aayu": "true\nfalse",
    "005_comparison.aayu": "true\nfalse\ntrue\ntrue\ntrue\ntrue",
    "006_if.aayu": "Greater",
    "007_while.aayu": "15",
    "008_functions.aayu": "30",
    "009_recursion.aayu": "120",
    "010_arrays.aayu": "2",
    "011_dictionaries.aayu": "AAYU",
    "012_strings.aayu": "AAYU",
    "013_modules.aayu": "<Module math>",
    "014_errors.aayu": "Error",
    "015_filesystem.aayu": "content",
    "016_http.aayu": "200",
    "017_database.aayu": "AAYU_USER"
}

def main():
    import sys
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    print("=======================================")
    print(" AAYU Language Conformance Suite       ")
    print("=======================================\n")
    
    runtime_exe = os.path.join("runtime", "native", "aayu-runtime.exe")
    if not os.path.exists(runtime_exe):
        print(f"[!] Warning: {runtime_exe} not found. Did you build the VM?")
        print("[!] Please run `python build_runtime.py` first.\n")
        sys.exit(1)

    tests_dir = os.path.join("tests", "conformance")
    test_files = sorted(glob.glob(os.path.join(tests_dir, "*.aayu")))
    
    results = {
        "PASS": [],
        "FAIL": [],
        "CRASH": [],
        "NOT IMPLEMENTED": []
    }
    
    for test_path in test_files:
        test_name = os.path.basename(test_path)
        if test_name not in EXPECTED:
            continue
        test_path = test_path.replace("\\", "/")
        print(f"Testing {test_name}... ", end="", flush=True)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            bytecode_path = os.path.join(tmpdir, test_name.replace(".aayu", ".aybc"))
            
            compile_result = subprocess.run([sys.executable, "-m", "aayu.cli", "build", test_path, "-o", bytecode_path], capture_output=True, text=True)
            
            if compile_result.returncode != 0:
                if "NotImplemented" in compile_result.stderr or "Syntax Error" in compile_result.stderr:
                    results["NOT IMPLEMENTED"].append(test_name)
                    print("NOT IMPLEMENTED")
                else:
                    results["CRASH"].append((test_name, "Compiler Crash\n" + compile_result.stderr))
                    print("COMPILER CRASH")
                continue
                
            # 2. Run bytecode on Native VM with timeout
            try:
                run_result = subprocess.run([runtime_exe, bytecode_path], capture_output=True, text=True, timeout=5)
            except subprocess.TimeoutExpired:
                results["CRASH"].append((test_name, "TIMEOUT (Infinite Loop?)"))
                print("TIMEOUT")
                continue
        
        if run_result.returncode != 0:
            if "unknown opcode" in run_result.stderr.lower():
                results["NOT IMPLEMENTED"].append(test_name)
                print("NOT IMPLEMENTED")
            else:
                results["CRASH"].append((test_name, run_result.stderr.strip()))
                print("CRASH")
            continue
            
        output = run_result.stdout.strip()
        expected = EXPECTED[test_name].strip()
        
        if output == expected:
            results["PASS"].append(test_name)
        else:
            results["FAIL"].append((test_name, expected, output))
            
    print("=======================================")
    print(" AAYU Language Conformance Score")
    print("=======================================\n")
    
    if results["PASS"]:
        print("PASS")
        for name in results["PASS"]:
            print(f"  {name}")
        print()
        
    if results["FAIL"]:
        print("FAIL")
        for name, exp, got in results["FAIL"]:
            print(f"  {name}")
            print(f"    Expected: {repr(exp)}")
            print(f"    Got:      {repr(got)}")
        print()
        
    if results["CRASH"]:
        print("CRASH")
        for name, err in results["CRASH"]:
            print(f"  {name}")
            print(f"    Error: {err}")
        print()
        
    if results["NOT IMPLEMENTED"]:
        print("NOT IMPLEMENTED")
        for name in results["NOT IMPLEMENTED"]:
            print(f"  {name}")
        print()

    total_tests = sum(len(v) for v in results.values())
    total_passed = len(results["PASS"])
    score = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    
    print("=======================================")
    print(f" Overall Conformance: {total_passed} / {total_tests} Features ({score:.0f}%)")
    print("=======================================\n")
    
    print("Release Status:")
    if total_passed == total_tests and total_tests > 0:
        print("✅ PHASE 11A VERIFIED\n")
    else:
        print("❌ DO NOT RELEASE\n")
    
    if results["FAIL"] or results["CRASH"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
