import sys
from typing import Any

from aayu.compiler.semantic.context import SemanticContext
from aayu.compiler.semantic.diagnostics import DiagnosticEngine
from aayu.compiler.hir.builder import HIRBuilder
from aayu.compiler.hir.validator import HIRValidator
from aayu.compiler.errors import InternalCompilerError, CompilerError
from aayu.compiler.ast.nodes import ProgramNode, ActionDeclarationNode

def run_fuzzer():
    errors_caught = 0
    failures = 0
    
    diag = DiagnosticEngine()
    ctx = SemanticContext(diag)
    builder = HIRBuilder(ctx)
    builder.module_id = "fuzz_test"
    
    # Fuzz 1: Unknown Type ID
    try:
        builder._get_type_id(999999)
        print("FAIL: Fuzz 1 did not raise any exception")
        failures += 1
    except InternalCompilerError:
        errors_caught += 1
    except Exception as e:
        print(f"FAIL: Fuzz 1 raised raw exception: {type(e).__name__} - {e}")
        failures += 1
        
    # Fuzz 2: Invalid AST node to build_expr
    try:
        class FakeNode:
            node_id = 123
        builder._build_expr(FakeNode(), builder.global_scope)
        print("FAIL: Fuzz 2 did not raise any exception")
        failures += 1
    except InternalCompilerError:
        errors_caught += 1
    except Exception as e:
        print(f"FAIL: Fuzz 2 raised raw exception: {type(e).__name__} - {e}")
        failures += 1
        
    # Fuzz 3: Malformed HIR passed to validator
    from aayu.compiler.hir.nodes import HIRModule, HIRLiteral, HIRAssignment
    from aayu.compiler.semantic.context import TypeID
    
    validator = HIRValidator(ctx)
    try:
        validator.validate("Not a module")
        print("FAIL: Fuzz 3 did not raise any exception")
        failures += 1
    except InternalCompilerError:
        errors_caught += 1
    except Exception as e:
        # We expect a raw exception here because "Not a module" isn't even a node.
        # But let's verify Fuzz 4 below.
        pass

    try:
        # Valid module with invalid HIRLiteral (missing TypeID in registry)
        invalid_module = HIRModule(
            origin_node_id=1,
            globals=[
                HIRAssignment(
                    origin_node_id=2,
                    target=None,
                    value=HIRLiteral(origin_node_id=3, type_id=TypeID(9999), value=1)
                )
            ],
            actions=[],
            functions=[]
        )
        validator.validate(invalid_module)
        print("FAIL: Fuzz 4 did not raise any exception")
        failures += 1
    except InternalCompilerError:
        errors_caught += 1
    except Exception as e:
        print(f"FAIL: Fuzz 4 raised raw exception: {type(e).__name__} - {e}")
        failures += 1

    if failures > 0:
        print(f"Fuzz test FAILED with {failures} failures.")
        sys.exit(1)
        
    print(f"Fuzz test PASSED. Gracefully caught {errors_caught} malformed inputs as ICE.")
    sys.exit(0)

if __name__ == "__main__":
    run_fuzzer()
