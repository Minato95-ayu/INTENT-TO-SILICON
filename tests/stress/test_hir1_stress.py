import unittest
import time
import tracemalloc
from aayu.compiler.ast.nodes import reset_node_counter
from aayu.compiler.parser import Parser
from aayu.compiler.semantic.scope_pass import ScopePass
from aayu.compiler.hir.builder import HIRBuilder

class TestHIR1Stress(unittest.TestCase):
    def setUp(self):
        reset_node_counter()
        
    def test_performance_and_memory_budgets(self):
        # Generate a massive source string with 10,000 assignments
        source_lines = ["state x = 0", "action massive"]
        for i in range(10000):
            source_lines.append(f"  x = {i}")
        source_lines.append("end")
        source = "\n".join(source_lines)
        
        # We only measure the HIR generation phase, not parsing, since this is HIR stress test.
        # However, to be strict with the Compiler Pipeline, we'll measure AST -> HIR
        
        from aayu.compiler.lexer import Lexer
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        from aayu.compiler.semantic.pipeline import SemanticPipeline
        
        tracemalloc.start()
        t0 = time.time()
        hir = SemanticPipeline().run(ast)
        t1 = time.time()
        
        self.assertIsNotNone(hir, "Semantic validation should not fail")
        
        # Validation Phase
        from aayu.compiler.hir.validator import HIRValidator
        validator = HIRValidator()
        
        t2 = time.time()
        validator.validate(hir)
        t3, peak = time.time(), tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        
        duration_ms = (t1 - t0) * 1000
        peak_mb = peak / (1024 * 1024)
        
        # Rule 24: Performance & Memory Regression Rule
        # Budget: < 2000 ms for 10k nodes
        # Budget: < 40 MB for 10k nodes
        self.assertLess(duration_ms, 2000, f"Performance Regression: HIR Generation took {duration_ms:.2f} ms (> 2000ms)")
        self.assertLess(peak_mb, 40, f"Memory Regression: HIR Generation took {peak_mb:.2f} MB (> 40MB)")
        print(f"\\nHIR Stress Passed: {duration_ms:.2f}ms, {peak_mb:.2f}MB")

if __name__ == '__main__':
    unittest.main()
