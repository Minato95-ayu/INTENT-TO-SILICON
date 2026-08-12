import unittest
import json
import os
import dataclasses
from aayu.compiler.ast.nodes import reset_node_counter
from aayu.compiler.parser import Parser
from aayu.compiler.semantic.scope_pass import ScopePass
from aayu.compiler.hir.builder import HIRBuilder
from aayu.compiler.hir.validator import HIRValidator
from aayu.compiler.hir.nodes import _global_hir_counter

# Reset counters for deterministic testing
def reset_counters():
    reset_node_counter()
    import itertools
    global _global_hir_counter
    # We must reset the module-level counter in nodes.py
    import aayu.compiler.hir.nodes as hir_nodes
    hir_nodes._global_hir_counter = itertools.count(1)

class TestHIR1Pipeline(unittest.TestCase):
    def setUp(self):
        reset_counters()
        self.snapshot_dir = os.path.join(os.path.dirname(__file__), "..", "golden", "hir")
        os.makedirs(self.snapshot_dir, exist_ok=True)

    def _compile_to_hir(self, source: str):
        # 1. Lex and Parse
        from aayu.compiler.lexer import Lexer
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 2. Semantic and HIR Build
        from aayu.compiler.semantic.pipeline import SemanticPipeline
        pipeline = SemanticPipeline()
        hir = pipeline.run(ast)
        
        if hir is None:
            errors = [d.message for d in pipeline.diag_engine.diagnostics]
            raise Exception(f"Semantic validation failed: {errors}")
            
        # Validation is now done inside pipeline.run
        return hir

    def _check_snapshot(self, test_name: str, hir_module):
        snapshot_file = os.path.join(self.snapshot_dir, f"{test_name}.json")
        
        # Convert to dict, but remove dynamic memory addresses if any
        hir_dict = dataclasses.asdict(hir_module)
        actual_json = json.dumps(hir_dict, indent=2, sort_keys=True)
        
        if not os.path.exists(snapshot_file) or os.environ.get("UPDATE_SNAPSHOTS") == "1":
            with open(snapshot_file, 'w') as f:
                f.write(actual_json)
            return
            
        with open(snapshot_file, 'r') as f:
            expected_json = f.read()
            
        self.assertEqual(expected_json, actual_json, f"HIR Snapshot Mismatch for {test_name}. Architecture Regression Detected.")

    def test_basic_assignment_and_action(self):
        source = """
        state counter = 0
        
        action increment
            counter = counter + 1
        end
        """
        hir = self._compile_to_hir(source)
        self._check_snapshot("basic_assignment_action", hir)

    def test_struct_and_enum_init(self):
        source = """
        enum Status { Active, Inactive }
        struct User { id: Int, status: Status }
        state u = User { id: 0, status: Status.Inactive }
        
        action create
            u = User { id: 1, status: Status.Active }
        end
        """
        hir = self._compile_to_hir(source)
        self._check_snapshot("struct_enum_init", hir)

if __name__ == '__main__':
    unittest.main()
