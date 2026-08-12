import unittest
import time
import psutil
import os
from aayu.compiler.lexer import Lexer
from aayu.compiler.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline
from aayu.compiler.hir.validator import HIRValidator
from aayu.compiler.ast.nodes import reset_node_counter
import aayu.compiler.hir.nodes as hir_nodes
import itertools

def reset_counters():
    reset_node_counter()
    hir_nodes._global_hir_counter = itertools.count(1)

class TestHIR2Stress(unittest.TestCase):
    def setUp(self):
        reset_counters()

    def test_stress_nested_loops_and_breaks(self):
        # Generate a deeply nested AST with loops, ifs, and breaks
        
        # We will nest loops 50 levels deep, with if/else branches and break/continues.
        
        source_lines = ["action stress_test"]
        source_lines.append("state counter = 0")
        
        depth = 50
        for i in range(depth):
            source_lines.append(f"{'  ' * (i+1)}while counter < 1000 {{")
            source_lines.append(f"{'  ' * (i+2)}if counter == {i} {{")
            source_lines.append(f"{'  ' * (i+3)}continue")
            source_lines.append(f"{'  ' * (i+2)}}} else {{")
            source_lines.append(f"{'  ' * (i+3)}counter = counter + 1")
            
        # Inner-most break
        source_lines.append(f"{'  ' * (depth+2)}break")
        
        for i in range(depth-1, -1, -1):
            source_lines.append(f"{'  ' * (i+2)}}}")
            source_lines.append(f"{'  ' * (i+1)}}}")
            
        source_lines.append("end")
        
        source = "\n".join(source_lines)
        
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        
        start_time = time.perf_counter()
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        pipeline = SemanticPipeline()
        hir = pipeline.run(ast)
        
        validator = HIRValidator()
        validator.validate(hir)
        
        end_time = time.perf_counter()
        mem_after = process.memory_info().rss
        
        duration_ms = (end_time - start_time) * 1000
        mem_used_mb = (mem_after - mem_before) / (1024 * 1024)
        
        print(f"\\nHIR-2 Stress Test Duration: {duration_ms:.2f}ms")
        print(f"Memory Used: {mem_used_mb:.2f}MB")
        
        self.assertLess(duration_ms, 2000, "Stress test exceeded 2000ms budget.")
        self.assertLess(mem_used_mb, 150, "Stress test exceeded 150MB memory budget.")

if __name__ == '__main__':
    unittest.main()
