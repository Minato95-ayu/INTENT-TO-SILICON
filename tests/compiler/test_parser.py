import unittest
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.ast.nodes import ProgramNode, StateDeclarationNode, LiteralNode, WidgetNode

class TestParser(unittest.TestCase):
    def test_parse_state_declaration(self):
        code = "state counter = 0"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        self.assertIsInstance(ast, ProgramNode)
        self.assertEqual(len(ast.statements), 1)
        
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, StateDeclarationNode)
        self.assertEqual(stmt.name, "counter")
        self.assertIsInstance(stmt.value, LiteralNode)
        self.assertEqual(stmt.value.value, "0")

    def test_parse_widget(self):
        code = '''
        page Home
            title "Hello World"
        end
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        self.assertEqual(len(ast.statements), 1)
        page = ast.statements[0]
        
        self.assertIsInstance(page, WidgetNode)
        self.assertEqual(page.widget_type, "Page")
        self.assertEqual(page.props["name"], "Home")
        
        self.assertEqual(len(page.children), 1)
        title = page.children[0]
        self.assertIsInstance(title, WidgetNode)
        self.assertEqual(title.widget_type, "title")
        self.assertEqual(title.props["text"], "Hello World")

if __name__ == '__main__':
    unittest.main()
