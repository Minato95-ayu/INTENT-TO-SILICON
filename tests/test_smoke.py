import json
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.session.manager import SessionManager

class AayuSmokeTests(unittest.TestCase):
    def compile_and_load(self, code, session_id="test-session"):
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        ast = SemanticAnalyzer().analyze(ast)
        
        pipeline = IRPipeline()
        hir = pipeline.to_hir(ast)
        mir = pipeline.to_mir(hir)
        lir = pipeline.to_lir(mir)
        
        prog = BytecodeEncoder().encode(lir)
        self.manager = SessionManager(prog)
        session = self.manager.get_or_create_session(session_id)
        return session

    def test_counter_state_and_concat(self):
        code = """
        Page Counter
            state count = 0
            state msg = "Count is: "
            
            action inc()
                count = count + 1
                msg = "Count is: " + count
            end
            
            Column
                Text msg
                Button "Inc" onClick=inc
            end
        end
        """
        session = self.compile_and_load(code, "counter-session")
        
        from runtime.renderers.web_renderer import serialize_node

        session.vm.call_action_by_name("Counter")
        tree = serialize_node(session.vm.interpreter.render_tree.root, set())
        
        def get_text_value(node):
            if node.get("type") == "text":
                return node.get("props", {}).get("value_node")
            for child in node.get("children", []):
                val = get_text_value(child)
                if val is not None:
                    return val
            return None

        self.assertEqual(str(get_text_value(tree)), "Count is: ")
        
        session.vm.call_action_by_name("inc")
        session.vm.call_action_by_name("Counter")
        tree = serialize_node(session.vm.interpreter.render_tree.root, set())
        self.assertEqual(str(get_text_value(tree)), "Count is: 1")
        
        session.vm.call_action_by_name("inc")
        session.vm.call_action_by_name("Counter")
        tree = serialize_node(session.vm.interpreter.render_tree.root, set())
        self.assertEqual(str(get_text_value(tree)), "Count is: 2")
        session.shutdown()

if __name__ == "__main__":
    unittest.main()

