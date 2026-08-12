import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.errors import DiagnosticEngine

def generate_valid_cases():
    cases = []
    # Apps
    cases.append('app "Shop"')
    
    # State
    cases.append('state x = 10.')
    cases.append('state { a = 1, b = 2 }')
    cases.append('state { a = "str", b = true }')
    
    # Let
    cases.append('let y = 100.')
    cases.append('let a = (10 + 2) * 5.')
    
    # Functions
    cases.append('fn add(a, b) { return a + b. }.')
    cases.append('fn empty() { }.')
    
    # Models
    cases.append('''model User {
        id: Int @primary
        name: String
        age: Int
    }.''')
    
    # If/While
    cases.append('if x > 10 { let y = 1. } else { let y = 2. }.')
    cases.append('while true { let x = 1. }.')
    
    # Widgets
    cases.append('''page Home {
        Text("Hello")
    }''')
    
    # More combinations
    for i in range(500):
        cases.append(f'let var_{i} = {i}.')
        cases.append(f'fn action_{i}() {{ let x = {i}. }}.')
        
    return cases
    
def generate_invalid_cases():
    cases = []
    # Missing terminator
    cases.append('let x = 10')
    cases.append('state x =')
    cases.append('fn broken(')
    cases.append('model Bad {')
    cases.append('if x > 10 let y = 1.')
    
    # Syntax errors
    for i in range(500):
        cases.append(f'let {i}var = {i}')
        cases.append(f'fn () {{ let x = {i} }}.')
        
    return cases

def run_tests():
    valid = generate_valid_cases()
    invalid = generate_invalid_cases()
    
    total = len(valid) + len(invalid)
    print(f"Running Grammar Test Suite on {total} cases...")
    
    passed_valid = 0
    passed_invalid = 0
    failed_valid = []
    
    import time
    start_time = time.time()
    
    for case in valid:
        diag = DiagnosticEngine()
        tokens = Lexer(case).tokenize()
        parser = Parser(tokens, diag=diag)
        parser.parse()
        if not diag.has_errors():
            passed_valid += 1
        else:
            err = diag.diagnostics[0] if diag.diagnostics else None
            msg = err.message if err else "Unknown Error"
            failed_valid.append((case, msg))
            
    for case in invalid:
        diag = DiagnosticEngine()
        try:
            tokens = Lexer(case).tokenize()
            parser = Parser(tokens, diag=diag)
            parser.parse()
            if diag.has_errors():
                passed_invalid += 1
        except Exception as e:
            # Fatal error means recovery failed or tokenizer crashed
            print(f"FATAL ERROR on invalid case:\n{case}\nError: {e}")
            pass
            
    end_time = time.time()
    avg_time = ((end_time - start_time) * 1000) / total
            
    print(f"Valid Cases Passed: {passed_valid}/{len(valid)}")
    print(f"Invalid Cases Handled Safely: {passed_invalid}/{len(invalid)}")
    
    if failed_valid:
        print("\n--- FAILING VALID CASES ---")
        for i, (case, msg) in enumerate(failed_valid[:10]):
            print(f"Failure #{i+1}")
            print(f"Reason: {msg}")
            print(f"Actual Code:\n{case}\n")
            
    with open(os.path.join(os.path.dirname(__file__), "grammar_coverage.txt"), "w") as f:
        f.write(f"{passed_valid+passed_invalid}/{total}/{len(invalid) - passed_invalid}/{avg_time:.2f}")
        
    if passed_valid == len(valid) and passed_invalid == len(invalid):
        return True
    return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
