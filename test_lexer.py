import sys
sys.path.insert(0, ".")
from compiler.lexer.lexer import Lexer
with open("demo_app.aayu") as f:
    code = f.read()
lexer = Lexer(code)
for t in lexer.tokenize():
    if 12 <= t.line <= 17:
        print(t)
