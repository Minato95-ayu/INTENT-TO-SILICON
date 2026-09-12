import unittest
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.vm.instructions import Opcode
from compiler.errors import CompilerError
from tests.compiler.test_helpers import CompilerE2EMixin

class TestR61BWidget(CompilerE2EMixin, unittest.TestCase):
    
    def execute_aayu(self, code: str) -> list[str]:
        # Override to bypass CFGBuilder for UI widgets
        from compiler.lexer.lexer import Lexer
        from compiler.parser.parser import Parser
        from compiler.semantic.analyzer import SemanticAnalyzer
        from compiler.ir.pipeline import IRPipeline
        from compiler.bytecode.encoder import BytecodeEncoder
        from runtime.session.manager import SessionManager
        import sys
        import io

        lexer = Lexer(code)
        ast = Parser(lexer.tokenize()).parse()
        semantic_ast = SemanticAnalyzer().analyze(ast)

        pipeline = IRPipeline()
        hir = pipeline.to_hir(semantic_ast)
        lir = pipeline.to_lir(pipeline.to_mir(hir))
        prog = BytecodeEncoder().encode(lir)

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            manager = SessionManager(prog)
            session = manager.get_or_create_session("test-session")
            session.vm.execute()
            raw_output = sys.stdout.getvalue()
        finally:
            if 'session' in locals():
                session.shutdown()
            sys.stdout = old_stdout

        lines = raw_output.strip().split('\n') if raw_output.strip() else []
        _TRACE_PREFIXES = ("[VM TRACE]", "[VM]", "[SessionManager]", "[DEBUG ENCODER]")
        lines = [line for line in lines if not any(line.startswith(prefix) for prefix in _TRACE_PREFIXES)]
        
        # In UI E2E tests, the output we want to verify is the generated widget tree on the node stack.
        def dump_node(node) -> str:
            if not hasattr(node, "type"): return str(node)
            props_str = ", ".join(f"{k}={repr(v)}" for k, v in sorted(node.props.items()))
            res = f"{node.type.upper()}({props_str})"
            for child in node.children:
                res += f" [{dump_node(child)}]"
            return res
            
        for node in session.vm.interpreter.node_stack:
            if node != "$BLOCK_START":
                lines.append(dump_node(node))
                
        return lines
    
    def _compile_to_bytecode(self, source: str):
        lexer = Lexer(source)
        ast = Parser(lexer.tokenize()).parse()
        semantic_ast = SemanticAnalyzer().analyze(ast)
        pipeline = IRPipeline()
        hir = pipeline.to_hir(semantic_ast)
        lir = pipeline.to_lir(pipeline.to_mir(hir))
        prog = BytecodeEncoder().encode(lir)
        return prog.bytecode

    def test_widget_dynamic_counts(self):
        """Test different dynamic property counts (N=0, 1, 2, 3) through E2E pipeline."""
        cases = [
            # N=0
            ("Text \"hello\"", "TEXT(text='hello')"),
            # N=1
            ("let x = 'world'\nText x", "TEXT(value_node='world')"),
            # N=2
            ("let x = 'a'\nlet y = 'b'\nText x color=y", "TEXT(color='b', value_node='a')"),
            # N=3
            ("let x = 'a'\nlet y = 'b'\nlet z = 'c'\nText x color=y size=z", "TEXT(color='b', size='c', value_node='a')")
        ]
        
        for source, expected in cases:
            # We wrap it in a column to ensure it gets rendered to the tree
            full_source = f"action App()\nColumn\n{source}\nend\nend\n"
            result = self.execute_aayu(full_source)
            self.assertTrue(any(expected in r for r in result) or (not result and expected == ""), f"Expected {expected} in {result}")

    def test_isa_operand_encoding(self):
        """Verify the exact 16-bit operand packed with widget_type_id and dynamic_prop_count."""
        # WIDGET_TYPES["TEXT"] = 6
        # 1 dynamic property (x) -> count = 1
        # operand should be: (6 << 8) | 1 = 0x0601 = 1537
        source = "action App()\nColumn\nlet x = 1\nText x\nend\nend\n"
        bytecode = self._compile_to_bytecode(source)
        
        has_build_widget = False
        i = 0
        while i < len(bytecode):
            if bytecode[i] == 0x50:  # BUILD_WIDGET
                has_build_widget = True
                operand = (bytecode[i+1] << 8) | bytecode[i+2]
                self.assertEqual(operand, 1537)
                break
            i += 3
            
        self.assertTrue(has_build_widget, "Bytecode must contain BUILD_WIDGET")

    def test_max_dynamic_props(self):
        """Verify that attempting to use > 255 dynamic properties throws a CompilerError."""
        # Generate a massive widget with 256 dynamic properties inline
        props = " ".join([f"p{i}=x" for i in range(256)])
        source = f"action App()\nColumn\nlet x = 1\nText {props}\nend\nend\n"
        
        with self.assertRaisesRegex(CompilerError, "too many dynamic properties"):
            self._compile_to_bytecode(source)

    def test_nested_widgets_and_stack(self):
        """Verify that nested widgets with a mix of static/dynamic props evaluate correctly."""
        source = """
        action App()
            Column
                let title = "My App"
                let btnColor = "red"
                Column spacing=10
                    Heading title
                    Button "Click" color=btnColor
                    Text "Static"
                end
            end
        end

        """
        result = self.execute_aayu(source)
        output = "".join(result)
        self.assertIn("HEADING(value_node='My App')", output)
        self.assertIn("BUTTON(color='red', text='Click')", output)
        self.assertIn("TEXT(text='Static')", output)

if __name__ == '__main__':
    unittest.main()
