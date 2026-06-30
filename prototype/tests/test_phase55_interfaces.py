import unittest
from lexer import Lexer
from parser import Parser
from compiler_context import CompilerContext
from passes.semantic.scope_builder import ScopeBuilderPass
from passes.semantic.type_checker import TypeCheckerPass
from passes.semantic.symbol_binding import SymbolBindingPass
from resolver.symbols import SymbolTable, ScopeType, SymbolKind, InterfaceSymbol
from resolver.semantic_types import InterfaceType, BuiltinTypes, FunctionType

class TestInterfaces(unittest.TestCase):
    def _run_type_checker(self, source: str) -> CompilerContext:
        ctx = CompilerContext()
        ctx.current_module = "test"
        ctx.symbol_tables["test"] = SymbolTable("test", ScopeType.GLOBAL)
        
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), "test.aayu")
        ast = parser.parse()
        
        ctx.ast = ast
        ctx.asts["test"] = ast
        
        ScopeBuilderPass().run(ctx)
        SymbolBindingPass().run(ctx)
        TypeCheckerPass().run(ctx)
        return ctx

    def test_interface_parsing_and_resolution(self):
        source = """
        interface Logger
            function log(message: Text): Void.
            function get_level(): Number.
        end.
        """
        ctx = self._run_type_checker(source)
        self.assertFalse(ctx.diagnostics.has_errors(), f"Errors: {ctx.diagnostics.diagnostics}")
        
        sym = ctx.symbol_tables["test"].lookup("Logger")
        self.assertIsNotNone(sym)
        self.assertIsInstance(sym, InterfaceSymbol)
        self.assertEqual(sym.kind, SymbolKind.INTERFACE)
        
        # Verify InterfaceType
        self.assertIsInstance(sym.resolved_type, InterfaceType)
        self.assertEqual(sym.resolved_type.name, "Logger")
        self.assertEqual(len(sym.resolved_type.methods), 2)
        
        # Verify method signatures
        log_method = sym.resolved_type.methods["log"]
        self.assertEqual(len(log_method.param_types), 1)
        self.assertEqual(log_method.param_types[0], BuiltinTypes.Text)
        self.assertEqual(log_method.return_type, BuiltinTypes.Void)
        
        get_level_method = sym.resolved_type.methods["get_level"]
        self.assertEqual(len(get_level_method.param_types), 0)
        self.assertEqual(get_level_method.return_type, BuiltinTypes.Number)

    def test_interface_type_annotation(self):
        source = """
        interface Writer
            function write(data: Text): Void.
        end.
        
        function do_test(w: Writer): Void
        end.
        """
        ctx = self._run_type_checker(source)
        self.assertFalse(ctx.diagnostics.has_errors(), f"Errors: {ctx.diagnostics.diagnostics}")
        
        sym = ctx.symbol_tables["test"].lookup("do_test")
        self.assertIsNotNone(sym)
        # Function types are currently just their return types or missing in Phase 5.4, 
        # so we get the AST node to check the parameter's resolved type.
        func_node = None
        for stmt in ctx.ast.statements:
            if getattr(stmt, "name", "") == "do_test":
                func_node = stmt
                break
        
        param_sym = func_node.func_scope.lookup("w")
        self.assertIsNotNone(param_sym)
        self.assertIsInstance(param_sym.resolved_type, InterfaceType)
        self.assertEqual(param_sym.resolved_type.name, "Writer")

    def test_nominal_subtyping(self):
        source = """
        interface Animal
            function speak(): Void.
        end.
        
        interface Dog
            function speak(): Void.
            function bark(): Void.
        end.
        
        function check_subtyping(d: Dog): Void
            let a: Animal is d.
        end.
        """
        ctx = self._run_type_checker(source)
        self.assertTrue(ctx.diagnostics.has_errors())
        # For Phase 5.5, nominal subtyping requires exact match. 
        # So 'Dog' cannot be assigned to 'Animal' even if it matches structurally.
        err = ctx.diagnostics.diagnostics[0]
        self.assertIn("AAYU2001", err.message)

if __name__ == '__main__':
    unittest.main()
