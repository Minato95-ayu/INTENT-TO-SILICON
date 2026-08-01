import sys
from aayu.compiler.parser.parser import Parser
from aayu.compiler.lexer.lexer import Lexer
import traceback

with open('ecommerce.aayu', 'r') as f:
    code = f.read()

try:
    l = Lexer(code).tokenize()
    Parser(l).parse()
    print("Parsed successfully!")
except Exception as e:
    if hasattr(e, 'line'):
        print(f"Error on line {e.line}, column {e.column}")
    traceback.print_exc()
