import os
import sys

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.errors import InternalCompilerError, CompilerError

if __name__ == "__main__":
    files = ["examples/ecommerce.aayu", "examples/school.aayu", "examples/blog.aayu", "examples/hospital.aayu"]

    all_ok = True
    tested = 0
    
    for file in files:
        if os.path.exists(file):
            tested += 1
            print(f"Running pipeline on {file} ...")
            try:
                with open(file, "r", encoding="utf-8") as f:
                    source = f.read()
                
                lexer = Lexer(source)
                tokens = lexer.tokenize()
                pipeline = SemanticPipeline()
                parser = Parser(tokens, diag=pipeline.diag_engine)
                ast = parser.parse()
                
                hir = pipeline.run(ast)
                
                if pipeline.diag_engine.has_errors():
                    print("  Diagnostic Errors:")
                    pipeline.diag_engine.print_all()
                else:
                    if hir:
                        print(f"  OK (HIR size: {len(hir.globals)} globals, {len(hir.actions)} actions)")
                    else:
                        print("  FAILED (No HIR generated)")
                        all_ok = False
            except InternalCompilerError as ice:
                print(f"  ICE CAUGHT: {ice}")
                all_ok = False
            except CompilerError as ce:
                print(f"  Diagnostic Error: {ce}")
            except Exception as e:
                print(f"  RAW EXCEPTION (FAIL): {e}")
                all_ok = False
                
    if tested == 0:
        print("No test files found.")
        sys.exit(1)
        
    sys.exit(0 if all_ok else 1)

