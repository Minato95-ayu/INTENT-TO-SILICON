"""
=============================================================================
FILE: test_phase45_modules.py
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
prototype_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'prototype'))
sys.path.insert(0, prototype_dir)
sys.path.insert(0, os.path.join(prototype_dir, 'language'))

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.passes.manager import PassManager
from compiler.frontend.passes.semantic.scope_builder import ScopeBuilderPass
from compiler.frontend.passes.semantic.import_binding import ImportBindingPass
from compiler.frontend.passes.semantic.symbol_binding import SymbolBindingPass
from compiler.frontend.passes.semantic.export_validation import ExportValidationPass
from compiler.frontend.compiler_context import CompilerContext
from compiler.frontend.resolver.symbols import SymbolTable, ScopeType

def validate_sources(sources):
    context = CompilerContext()
    for name, code in sources.items():
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize(), filename=name)
        ast = parser.parse()
        mod_name = name.replace(".aayu", "")
        context.asts[mod_name] = ast
        context.symbol_tables[mod_name] = SymbolTable(mod_name, ScopeType.MODULE)
        
    pm = PassManager()
    pm.add_pass(ScopeBuilderPass())
    pm.add_pass(ImportBindingPass())
    pm.add_pass(SymbolBindingPass())
    pm.add_pass(ExportValidationPass())
    
    # We must run passes per AST module, simulating ModuleResolverPass if needed
    for mod_name, ast in context.asts.items():
        context.current_module = mod_name
        pm.run(context)
        
    return context

def test_visibility_and_aliasing():
    # Create module 'math'
    math_code = """
    module math.
    
    public function calc_add(a, b)
        return a + b.
    end.
    
    private function calc_sub(a, b)
        return a - b.
    end.
    
    public let PI is 3.14.
    private let E is 2.71.
    """
    
    # Create main module (should fail)
    main_fail_code = """
    module main_fail.
    import math as m.
    
    public function execute()
        let sum is m.calc_sub(5, 5).
    end.
    """
    
    try:
        context_fail = validate_sources({"math.aayu": math_code, "main_fail.aayu": main_fail_code})
        if context_fail.diagnostics.has_errors():
            print("Private access violation correctly caught:")
            context_fail.diagnostics.print_all()
        else:
            print("ERROR: Private access violation NOT caught!")
            
        # Test 2: Selective Imports
        main_code_2 = """
        module main2.
        import math::{calc_add as plus, PI}.
        
        public function execute()
            let sum is plus(10, 10).
            let p is PI.
        end.
        """
        context2 = validate_sources({"math.aayu": math_code, "main2.aayu": main_code_2})
        if context2.diagnostics.has_errors():
            print("Selective import validation failed:")
            context2.diagnostics.print_all()
        else:
            print("Selective import validation successful!")
        
        # Test 3: Export Block
        utils_code = """
        module utils.
        
        function helper1()
            return 1.
        end.
        
        function helper2()
            return 2.
        end.
        
        export { helper1, helper2 }.
        """
        context3 = validate_sources({"utils.aayu": utils_code})
        if context3.diagnostics.has_errors():
            print("Export block validation failed:")
            context3.diagnostics.print_all()
        else:
            print("Export block validation successful!")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")

if __name__ == "__main__":
    test_visibility_and_aliasing()
