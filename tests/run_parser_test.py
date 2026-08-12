import sys
import os

# Add INTENT-TO-SILICON to sys.path so we can import aayu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.errors import DiagnosticEngine

def main():
    source_path = os.path.join(os.path.dirname(__file__), "test_parser_recovery.aayu")
    with open(source_path, "r") as f:
        source = f.read()

    diag = DiagnosticEngine()
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, diag=diag)
    
    print("Compiling test_parser_recovery.aayu...")
    
    ast = parser.parse()
    
    print("\n--- Diagnostics ---")
    diag.print_all()
    print("-------------------")
    
    if diag.has_errors():
        print(f"Compilation finished with {len(diag.diagnostics)} errors as expected.")
    else:
        print("Compilation succeeded (unexpected!).")

if __name__ == "__main__":
    main()
