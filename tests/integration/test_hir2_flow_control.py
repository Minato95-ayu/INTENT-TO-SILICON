import unittest
import json
import os
import dataclasses
from aayu.compiler.ast.nodes import reset_node_counter
from aayu.compiler.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.hir.validator import HIRValidator
from aayu.compiler.hir.nodes import _global_hir_counter

def reset_counters():
    reset_node_counter()
    import itertools
    global _global_hir_counter
    import aayu.compiler.hir.nodes as hir_nodes
    hir_nodes._global_hir_counter = itertools.count(1)

class TestHIR2FlowControl(unittest.TestCase):
    def setUp(self):
        reset_counters()
        self.snapshot_dir = os.path.join(os.path.dirname(__file__), "..", "golden", "hir")
        os.makedirs(self.snapshot_dir, exist_ok=True)

    def _compile_to_hir(self, source: str):
        from aayu.compiler.lexer import Lexer
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        pipeline = SemanticPipeline()
        hir = pipeline.run(ast)
        
        if hir is None:
            errors = [d.message for d in pipeline.diag_engine.diagnostics]
            raise Exception(f"Semantic validation failed: {errors}")
            
        validator = HIRValidator()
        validator.validate(hir)
            
        return hir

    def _check_snapshot(self, test_name: str, hir_module):
        snapshot_file = os.path.join(self.snapshot_dir, f"{test_name}.json")
        
        hir_dict = dataclasses.asdict(hir_module)
        actual_json = json.dumps(hir_dict, indent=2, sort_keys=True)
        
        if not os.path.exists(snapshot_file) or os.environ.get("UPDATE_SNAPSHOTS") == "1":
            with open(snapshot_file, 'w') as f:
                f.write(actual_json)
            return
            
        with open(snapshot_file, 'r') as f:
            expected_json = f.read()
            
        self.assertEqual(expected_json, actual_json, f"HIR Snapshot Mismatch for {test_name}.")

    def test_flow_control(self):
        source = """
        action test_loops
            state i = 0
            while i < 10 {
                if i == 5 {
                    break
                } else {
                    i = i + 1
                    continue
                }
            }
        end
        """
        hir = self._compile_to_hir(source)
        self._check_snapshot("flow_control_break_continue", hir)

    def test_invalid_break(self):
        source = """
        action test_invalid
            break
        end
        """
        with self.assertRaisesRegex(Exception, "Semantic validation failed:.*'break' can only be used inside a loop."):
            self._compile_to_hir(source)

    def test_invalid_continue(self):
        source = """
        action test_invalid
            continue
        end
        """
        with self.assertRaisesRegex(Exception, "Semantic validation failed:.*'continue' can only be used inside a loop."):
            self._compile_to_hir(source)

if __name__ == '__main__':
    unittest.main()
