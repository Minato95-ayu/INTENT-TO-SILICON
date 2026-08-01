import unittest
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.lexer.tokens import TokenType

class TestLexer(unittest.TestCase):
    def test_basic_tokens(self):
        code = "state counter = 0"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        self.assertEqual(len(tokens), 5) # state, counter, =, 0, EOF
        self.assertEqual(tokens[0].type, TokenType.KEYWORD)
        self.assertEqual(tokens[0].value, "state")
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].value, "counter")
        self.assertEqual(tokens[2].type, TokenType.OPERATOR)
        self.assertEqual(tokens[2].value, "=")
        self.assertEqual(tokens[3].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].value, "0")
        self.assertEqual(tokens[4].type, TokenType.EOF)

    def test_ui_keywords(self):
        code = '''page Home
title "Hello"
end'''
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        types = [t.type for t in tokens]
        self.assertIn(TokenType.KEYWORD, types)
        self.assertIn(TokenType.STRING, types)
        
        page_token = tokens[0]
        self.assertEqual(page_token.value, "page")
        
        string_token = tokens[3]
        self.assertEqual(string_token.type, TokenType.STRING)
        self.assertEqual(string_token.value, "Hello")

    def test_ignore_whitespace_and_comments(self):
        code = '''
        # This is a comment
        state a = 1
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        self.assertEqual(len(tokens), 5) # state, a, =, 1, EOF

    def test_symbols(self):
        code = "a += 1; ( ) { }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        vals = [t.value for t in tokens]
        self.assertIn("+=", vals)
        self.assertIn(";", vals)
        self.assertIn("(", vals)
        self.assertIn("{", vals)

if __name__ == '__main__':
    unittest.main()
