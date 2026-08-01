import json
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.session.manager import SessionManager

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

    def test_calculator_end_to_end(self):
        with open(os.path.join(os.path.dirname(__file__), "test_calculator.aayu"), "r") as f:
            code = f.read()

        session = self.compile_and_load(code, "calc-session")
        print(session.vm.action_addresses)
        
        from aayu.runtime.renderers.web_renderer import serialize_node
        
        # 1. Initial Page Load
        session.vm.call_action_by_name("Calculator")
        tree = serialize_node(session.vm.interpreter.render_tree.root, set())
        
        # Helper to find Text node value
        def get_text_value(node):
            if node.get("type") == "text":
                return node.get("props", {}).get("value_node")
            for child in node.get("children", []):
                val = get_text_value(child)
                if val is not None:
                    return val
            return None

        # Verify initial state is "0"
        self.assertEqual(str(get_text_value(tree)), "0")
        
        # 2. Press "7"
        session.vm.value_stack.push("7")
        session.vm.call_action_by_name("press")
        session.vm.call_action_by_name("Calculator")
        tree = serialize_node(session.vm.interpreter.render_tree.root, set())
        self.assertEqual(str(get_text_value(tree)), "7")
        
        # 3. Press "+"
        session.vm.value_stack.push("+")
        session.vm.call_action_by_name("pressOp")
        session.vm.call_action_by_name("Calculator")
        tree = serialize_node(session.vm.interpreter.render_tree.root, set())
        self.assertEqual(str(get_text_value(tree)), "0")
        
        # 4. Press "5"
        session.vm.value_stack.push("5")
        session.vm.call_action_by_name("press")
        session.vm.call_action_by_name("Calculator")
        tree = serialize_node(session.vm.interpreter.render_tree.root, set())
        self.assertEqual(str(get_text_value(tree)), "5")
        
        # 5. Press "="
        session.vm.call_action_by_name("calculate")
        session.vm.call_action_by_name("Calculator")
        tree = serialize_node(session.vm.interpreter.render_tree.root, set())
        print(f"DEBUG: op={session.vm.state_scopes[-1].get('op')}, previous={session.vm.state_scopes[-1].get('previous')}, current={session.vm.state_scopes[-1].get('current')}")
        print(f"DEBUG TREE: {json.dumps(tree, indent=2)}")
        self.assertEqual(str(get_text_value(tree)), "12.0")
        
        # 6. Press "C"
        session.vm.call_action_by_name("clear")
        session.vm.call_action_by_name("Calculator")
        tree = serialize_node(session.vm.interpreter.render_tree.root, set())
        print(f"DEBUG TREE AFTER CLEAR: {json.dumps(tree, indent=2)}")
        self.assertEqual(str(get_text_value(tree)), "0")

        # 7. Press "8", "-", "3", "="
        # 7. Press "8", "-", "3", "="
        session.vm.value_stack.push("8")
        session.vm.call_action_by_name("press")
        session.vm.value_stack.push("-")
        session.vm.call_action_by_name("pressOp")
        session.vm.value_stack.push("3")
        session.vm.call_action_by_name("press")
        session.vm.call_action_by_name("calculate")
        session.vm.call_action_by_name("Calculator")
        tree = serialize_node(session.vm.interpreter.render_tree.root, set())
        self.assertEqual(str(get_text_value(tree)), "5.0")

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
        
        from aayu.runtime.renderers.web_renderer import serialize_node

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

if __name__ == "__main__":
    unittest.main()
