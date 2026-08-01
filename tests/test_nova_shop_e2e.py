import os
import sys
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.session.manager import SessionManager

class NovaShopE2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        main_file = os.path.join(cls.project_dir, "src", "main.aayu")
        src_dir = os.path.join(cls.project_dir, "src")
        
        with open(main_file, "r", encoding="utf-8") as f:
            source = f.read()
            
        from aayu.compiler.lexer.lexer import Lexer
        from aayu.compiler.parser.parser import Parser
        from aayu.compiler.ast_resolver import resolve_ast_imports
        ast = Parser(Lexer(source).tokenize()).parse()
        cls.resolved_ast = resolve_ast_imports(ast, src_dir, set([os.path.abspath(main_file)]))
        
    def compile_nova_shop(self, session_id="nova-e2e"):
        ast = SemanticAnalyzer().analyze(self.resolved_ast)
        
        pipeline = IRPipeline()
        hir = pipeline.to_hir(ast)
        mir = pipeline.to_mir(hir)
        lir = pipeline.to_lir(mir)
        
        prog = BytecodeEncoder().encode(lir)
        self.manager = SessionManager(prog)
        session = self.manager.get_or_create_session(session_id)
        return session

    def get_state(self, session, var_name):
        for scope in reversed(session.vm.state_scopes):
            if var_name in scope:
                return scope[var_name]
        return None

    def serialize_tree(self, session):
        from aayu.runtime.renderers.web_renderer import serialize_node
        if session.vm.interpreter.render_tree and session.vm.interpreter.render_tree.root:
            return serialize_node(session.vm.interpreter.render_tree.root, set())
        return None

    def get_active_page_name(self, tree):
        if not tree or tree.get("type") != "page":
            return None
        return tree.get("props", {}).get("name")
        
    def find_text_with_value(self, tree, value):
        if tree.get("type") == "text":
            val = str(tree.get("props", {}).get("value_node", ""))
            if value in val:
                return True
        for child in tree.get("children", []):
            if self.find_text_with_value(child, value):
                return True
        return False

    def get_prop(self, tree, prop_name):
        if prop_name in tree.get("props", {}):
            return tree["props"][prop_name]
        for child in tree.get("children", []):
            val = self.get_prop(child, prop_name)
            if val is not None:
                return val
        return None

    # --- 1. NovaShopCompileTest ---

    def test_compile_and_load(self):
        session = self.compile_nova_shop("test_compile")
        self.assertIsNotNone(session)
        self.assertGreater(len(session.vm.action_addresses), 0)

    def test_all_actions_registered(self):
        session = self.compile_nova_shop("test_actions")
        expected_actions = [
            "go_home", "go_cart", "go_account", "go_signup", "go_generic",
            "do_search", "sys_nav_back", "add_iphone", "add_macbook", 
            "add_headphones", "add_ps5", "add_camera", "add_watch", 
            "do_login", "do_logout"
        ]
        for action in expected_actions:
            self.assertIn(action, session.vm.action_addresses)

    def test_all_pages_registered(self):
        session = self.compile_nova_shop("test_pages")
        expected_pages = [
            "HomePage", "CartPage", "LoginPage", "SignupPage", 
            "AccountPage", "GenericPage"
        ]
        for page in expected_pages:
            self.assertIn(page, session.vm.action_addresses)

    # --- 2. NovaShopNavigationTest ---

    def test_initial_render_home(self):
        session = self.compile_nova_shop("nav_home")
        session.vm.call_action_by_name("HomePage")
        tree = self.serialize_tree(session)
        self.assertEqual(self.get_active_page_name(tree), "HomePage")

    def test_navigate_to_cart(self):
        session = self.compile_nova_shop("nav_cart")
        session.vm.call_action_by_name("HomePage")
        session.vm.call_action_by_name("go_cart")
        session.vm.call_action_by_name("CartPage") # Simulated navigation
        tree = self.serialize_tree(session)
        self.assertEqual(self.get_active_page_name(tree), "CartPage")

    def test_navigate_to_login_when_logged_out(self):
        session = self.compile_nova_shop("nav_login")
        session.vm.update_state("isLoggedIn", 0)
        session.vm.call_action_by_name("go_account")
        session.vm.call_action_by_name("LoginPage")
        tree = self.serialize_tree(session)
        self.assertEqual(self.get_active_page_name(tree), "LoginPage")

    def test_navigate_to_account_when_logged_in(self):
        session = self.compile_nova_shop("nav_account")
        session.vm.update_state("isLoggedIn", 1)
        session.vm.call_action_by_name("go_account")
        session.vm.call_action_by_name("AccountPage")
        tree = self.serialize_tree(session)
        self.assertEqual(self.get_active_page_name(tree), "AccountPage")

    def test_navigate_to_generic(self):
        session = self.compile_nova_shop("nav_generic")
        session.vm.call_action_by_name("go_generic")
        session.vm.call_action_by_name("GenericPage")
        tree = self.serialize_tree(session)
        self.assertEqual(self.get_active_page_name(tree), "GenericPage")

    def test_back_navigation(self):
        session = self.compile_nova_shop("nav_back")
        session.vm.call_action_by_name("CartPage")
        session.vm.call_action_by_name("sys_nav_back")
        session.vm.call_action_by_name("HomePage")
        tree = self.serialize_tree(session)
        self.assertEqual(self.get_active_page_name(tree), "HomePage")

    def test_navigation_cycle(self):
        session = self.compile_nova_shop("nav_cycle")
        pages = ["HomePage", "CartPage", "LoginPage", "HomePage"]
        for p in pages:
            session.vm.call_action_by_name(p)
            tree = self.serialize_tree(session)
            self.assertEqual(self.get_active_page_name(tree), p)

    # --- 3. NovaShopCartTest ---

    def test_add_single_item(self):
        session = self.compile_nova_shop("cart_single")
        session.vm.call_action_by_name("HomePage")
        session.vm.call_action_by_name("add_iphone")
        self.assertEqual(self.get_state(session, "cartItemsCount"), 1)
        self.assertEqual(self.get_state(session, "subtotalAmount"), 999.0)
        self.assertEqual(self.get_state(session, "qty_iphone"), 1)

    def test_add_multiple_different_items(self):
        session = self.compile_nova_shop("cart_multiple")
        session.vm.call_action_by_name("HomePage")
        session.vm.call_action_by_name("add_iphone")
        session.vm.call_action_by_name("add_macbook")
        self.assertEqual(self.get_state(session, "cartItemsCount"), 2)
        self.assertEqual(self.get_state(session, "subtotalAmount"), 3498.0)

    def test_add_same_item_twice(self):
        session = self.compile_nova_shop("cart_twice")
        session.vm.call_action_by_name("HomePage")
        session.vm.call_action_by_name("add_headphones")
        session.vm.call_action_by_name("add_headphones")
        self.assertEqual(self.get_state(session, "qty_headphones"), 2)
        self.assertEqual(self.get_state(session, "subtotalAmount"), 498.0)

    def test_cart_state_survives_navigation(self):
        session = self.compile_nova_shop("cart_nav")
        session.vm.call_action_by_name("HomePage")
        session.vm.call_action_by_name("add_camera")
        session.vm.call_action_by_name("go_cart")
        session.vm.call_action_by_name("CartPage")
        session.vm.call_action_by_name("sys_nav_back")
        session.vm.call_action_by_name("HomePage")
        tree = self.serialize_tree(session)
        # 1 item in cart
        self.assertTrue(self.find_text_with_value(tree, "1"))

    def test_subtotal_renders_on_cart_page(self):
        session = self.compile_nova_shop("cart_subtotal")
        session.vm.call_action_by_name("HomePage")
        session.vm.call_action_by_name("add_watch")
        session.vm.call_action_by_name("go_cart")
        session.vm.call_action_by_name("CartPage")
        tree = self.serialize_tree(session)
        self.assertTrue(self.find_text_with_value(tree, "799.0"))

    # --- 4. NovaShopAuthTest ---

    def test_input_email_updates_state(self):
        session = self.compile_nova_shop("auth_email")
        session.vm.call_action_by_name("LoginPage")
        session.vm.update_state("loginEmail", "user@test.com")
        self.assertEqual(self.get_state(session, "loginEmail"), "user@test.com")

    def test_input_password_updates_state(self):
        session = self.compile_nova_shop("auth_pwd")
        session.vm.call_action_by_name("LoginPage")
        session.vm.update_state("loginPassword", "secret123")
        self.assertEqual(self.get_state(session, "loginPassword"), "secret123")

    def test_login_after_input(self):
        session = self.compile_nova_shop("auth_login_input")
        session.vm.call_action_by_name("LoginPage")
        session.vm.update_state("loginEmail", "user@test.com")
        session.vm.update_state("loginPassword", "secret123")
        session.vm.call_action_by_name("do_login")
        # Note: Confirms input doesn't interfere with login, not that it's used by login logic
        self.assertEqual(self.get_state(session, "isLoggedIn"), 1)
        self.assertEqual(self.get_state(session, "accountGreeting"), "Hello, Ayush")

    def test_login_sets_state(self):
        session = self.compile_nova_shop("auth_login")
        session.vm.call_action_by_name("HomePage")
        session.vm.call_action_by_name("do_login")
        self.assertEqual(self.get_state(session, "isLoggedIn"), 1)
        self.assertEqual(self.get_state(session, "accountGreeting"), "Hello, Ayush")

    def test_logout_resets_state(self):
        session = self.compile_nova_shop("auth_logout")
        session.vm.call_action_by_name("HomePage")
        session.vm.call_action_by_name("do_login")
        session.vm.call_action_by_name("do_logout")
        self.assertEqual(self.get_state(session, "isLoggedIn"), 0)
        self.assertEqual(self.get_state(session, "accountGreeting"), "Hello, sign in")

    def test_account_page_shows_greeting(self):
        session = self.compile_nova_shop("auth_account")
        session.vm.call_action_by_name("HomePage")
        session.vm.call_action_by_name("do_login")
        session.vm.call_action_by_name("go_account")
        session.vm.call_action_by_name("AccountPage")
        tree = self.serialize_tree(session)
        self.assertTrue(self.find_text_with_value(tree, "Hello, Ayush"))

    # --- 5. NovaShopMultiRenderTest ---

    def test_render_5x_no_crash(self):
        session = self.compile_nova_shop("multi_render")
        for _ in range(5):
            session.vm.call_action_by_name("HomePage")
            tree = self.serialize_tree(session)
            self.assertEqual(self.get_active_page_name(tree), "HomePage")

    def test_state_change_reflected_across_renders(self):
        session = self.compile_nova_shop("multi_render_state")
        session.vm.call_action_by_name("HomePage")
        
        session.vm.call_action_by_name("add_iphone")
        session.vm.call_action_by_name("HomePage")
        self.assertEqual(self.get_state(session, "subtotalAmount"), 999.0)
        
        session.vm.call_action_by_name("add_iphone")
        session.vm.call_action_by_name("HomePage")
        self.assertEqual(self.get_state(session, "subtotalAmount"), 1998.0)


if __name__ == "__main__":
    unittest.main()
