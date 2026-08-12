import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from aayu.compiler.lexer.lexer import Lexer

case = """page Home {
        Text(text="Hello")
    }"""

tokens = Lexer(case).tokenize()
for t in tokens:
    print(t.type, t.value)
