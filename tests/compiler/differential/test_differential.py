import pytest
from aayu.compiler.api import Compiler

# Placeholder tests for differential evaluation
# Compares Direct Interpreter vs Compiled Bytecode execution

def test_differential_addition():
    source = """
    app TestApp
    run
        a = 10
        b = 20
        c = a + b
    end
    """
    
    # 1. Compile to Bytecode and execute
    c1 = Compiler()
    assert c1.compile_text(source)
    # TODO: Capture output/state
    # c1.run()
    
    # 2. Direct AST/Interpreter Evaluation
    c2 = Compiler()
    assert c2.parse(source)
    assert c2.semantic()
    # TODO: Capture output/state using aayu.runtime.interpreter (AST Walk)
    
    # assert output1 == output2
    pass
