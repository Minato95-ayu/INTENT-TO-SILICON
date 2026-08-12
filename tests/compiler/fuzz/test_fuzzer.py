import pytest
import os
import random
from aayu.compiler.api import Compiler

def generate_random_ast_snippet(depth=0):
    """Recursively generates random valid (and somewhat invalid) AST structures."""
    if depth > 5:
        return f"{random.randint(0, 100)}"
        
    choice = random.choice(["assignment", "if", "while", "binary_op", "literal"])
    
    if choice == "assignment":
        var = f"var_{random.randint(0, 100)}"
        val = generate_random_ast_snippet(depth + 1)
        return f"{var} = {val}"
    elif choice == "if":
        cond = generate_random_ast_snippet(depth + 1)
        body = generate_random_ast_snippet(depth + 1)
        return f"if {cond}\n  {body}\nend"
    elif choice == "while":
        cond = generate_random_ast_snippet(depth + 1)
        body = generate_random_ast_snippet(depth + 1)
        return f"while {cond}\n  {body}\nend"
    elif choice == "binary_op":
        left = generate_random_ast_snippet(depth + 1)
        right = generate_random_ast_snippet(depth + 1)
        op = random.choice(["+", "-", "*", "/"])
        return f"{left} {op} {right}"
    else:
        return f"{random.randint(0, 100)}"

def test_fuzzer():
    # Number of iterations controlled by environment variable
    tier = os.environ.get("AAYU_FUZZ_TIER", "QUICK")
    
    if tier == "STRESS":
        iterations = 1_000_000
    elif tier == "NIGHTLY":
        iterations = 100_000
    else:
        iterations = 1000
        
    for i in range(iterations):
        source = f"""
        app FuzzTest{i}
        run
            {generate_random_ast_snippet()}
        end
        """
        
        # We don't assert compilation success, because random code is often invalid.
        # We assert that the compiler DOES NOT CRASH (no raw exceptions, only Graceful CompilerErrors)
        c = Compiler()
        c.compile_text(source)
