import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.type_pass import TypePass
from aayu.compiler.semantic.scope_pass import ScopePass
from aayu.compiler.semantic.symbols import SymbolTable, Symbol
from aayu.compiler.semantic.types import (
    Type, PrimitiveType, UnionType, OptionalType, make_nullable,
    T_INT, T_FLOAT, T_STRING, T_BOOL, T_ANY, T_NULL
)
from aayu.compiler.errors import DiagnosticEngine

class TestTypeParsing(unittest.TestCase):
    def test_parse_and_resolve_types(self):
        code = '''
        let a: Int = 5.
        let b: String? = null.
        let c: Int | Float = 10.
        let d: Optional<Int> = 1.
        '''
        tokens = Lexer(code).tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
    
        from aayu.compiler.semantic.pipeline import SemanticPipeline
        pipeline = SemanticPipeline()
        hir = pipeline.run(ast)
        
        diag = pipeline.diag_engine
        scope_pass = pipeline.scope_pass
        type_pass = pipeline.type_pass
        context = pipeline.context
        
        global_scope = scope_pass.global_scope
        
        sym_a = global_scope.resolve("a")
        self.assertEqual(sym_a.data_type, T_INT)
        
        sym_b = global_scope.resolve("b")
        self.assertEqual(sym_b.data_type, make_nullable(T_STRING))
        
        sym_c = global_scope.resolve("c")
        self.assertEqual(sym_c.data_type, UnionType(T_INT, T_FLOAT))
        
        sym_d = global_scope.resolve("d")
        self.assertEqual(sym_d.data_type, OptionalType(T_INT))

if __name__ == "__main__":
    unittest.main()
