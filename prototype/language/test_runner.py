import os
import sys
import glob
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, Environment
from ast_nodes import TestNode
from errors import AAYUError

def run_tests():
    # Find all .test.aayu files in tests/ directory
    test_files = glob.glob("tests/**/*.test.aayu", recursive=True)
    
    if not test_files:
        print("No tests found in tests/ directory.")
        return

    print(f"Running AAYU Tests...\n")
    
    passed = 0
    failed = 0
    failures = []

    for filepath in test_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source_code = f.read()

            lexer = Lexer(source_code)
            tokens = lexer.tokenize()

            parser = Parser(tokens, filename=os.path.basename(filepath))
            ast = parser.parse()

            interpreter = Interpreter(test_mode=True)
            
            # Since a test file might not have a main task, we just evaluate all top-level statements
            # But the actual test execution happens inside visit_TestNode
            for statement in ast.statements:
                if isinstance(statement, TestNode):
                    try:
                        interpreter.evaluate(statement)
                        # Ensure output respects ANSI
                        # If color supported, print green checkmark
                        print(f"\033[92m✓\033[0m {statement.name}")
                        passed += 1
                    except AAYUError as e:
                        print(f"\033[91m❌\033[0m {statement.name}")
                        failed += 1
                        failures.append((statement.name, filepath, e))
                else:
                    # Execute other top level code (e.g. use statements)
                    interpreter.evaluate(statement)

        except AAYUError as e:
            # Syntax error or import error in the test file itself
            print(f"Error parsing {filepath}:")
            use_color = sys.stdout.isatty() if hasattr(sys.stdout, 'isatty') else False
            print(e.format(use_color))
            sys.exit(1)
        except Exception as e:
            print(f"Internal error running {filepath}: {e}")
            sys.exit(1)

    print("")
    if failures:
        for name, filepath, err in failures:
            use_color = sys.stdout.isatty() if hasattr(sys.stdout, 'isatty') else False
            print(err.format(use_color))
            print("")

    print(f"{passed} passed")
    print(f"{failed} failed")

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    # Ensure UTF-8 output on Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
            
    run_tests()
