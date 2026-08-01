"""
=============================================================================
FILE: test_phase46_reflection.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import sys
import os

# Add prototype dir to path
prototype_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'prototype'))
sys.path.insert(0, prototype_dir)

from aayu.compiler.engine.api import AAYUEngine

def test_reflection():
    engine = AAYUEngine()
    
    code = """
    module main.
    
    public function hello()
        return "world".
    end.
    
    private function secret()
        return 42.
    end.
    
    export { hello }.
    """
    
    from aayu.compiler.lexer.lexer import Lexer
    from aayu.compiler.parser.parser import Parser
    from aayu.compiler.passes.lowering import LoweringPass
    from aayu.compiler.bytecode.encoder import BytecodeEncoder
    from aayu.runtime.vm.vm import VirtualMachine
    
    def compile_aayu(src, name):
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename=name)
        ast = parser.parse()
        lowering = LoweringPass()
        normalized_ast = lowering.lower(ast)
        compiler = BytecodeEncoder(filename=name)
        return compiler.compile(normalized_ast)
        
    # Compile module
    bytecode = compile_aayu(code, "main")
    
    # Find functions from bytecode constants to test runtime
    # Wait, instead of testing bytecode manually, let's just run an AAYU script that reflects on itself!
    
    script = """
    module test_reflect.
    
    public function target_func(a, b)
        return a + b.
    end.
    
    let val is 42.
    print(reflect_type_of(val)). # "Number"
    
    let s is "hello".
    print(reflect_type_of(s)). # "String"
    
    let f is target_func.
    print(reflect_type_of(f)). # "Function"
    print(reflect_module_of(f)). # "test_reflect"
    
    let info is reflect_inspect(f).
    print(map_get(info, "type")). # "Function"
    print(map_get(info, "name")). # "target_func"
    print(map_get(info, "visibility")). # "public"
    print(map_get(info, "parameter_count")). # 2
    print(map_get(info, "is_exported")). # false
    """
    
    bytecode2 = compile_aayu(script, "test_reflect")
    
    from aayu.runtime.vm.vm import VirtualMachine
    vm = VirtualMachine()
    try:
        vm.run(bytecode2)
    except Exception as e:
        print(f"Execution Error: {e}")
        raise e
        
    out = "".join(vm.output)
    print("Output:")
    print(out)
    
    assert "Number" in out
    assert "string" in out
    assert "Function" in out
    assert "test_reflect" in out
    assert "target_func" in out
    assert "public" in out
    assert "2" in out
    print("All reflection tests passed!")

if __name__ == "__main__":
    test_reflection()
