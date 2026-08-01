from aayu.compiler.lexer.lexer import Lexer
import sys
source = 'notes.push("Hello")'
lex = Lexer(source)
for t in lex.tokenize():
    print(t)
