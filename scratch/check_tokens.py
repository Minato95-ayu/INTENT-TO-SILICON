import sys
import os

# Add local directory to path
sys.path.insert(0, os.path.abspath('.'))

from aayu.compiler.lexer.lexer import Lexer

with open("examples/whatsapp_clone/main.aayu", "r") as f:
    source = f.read()

lexer = Lexer(source)
for t in lexer.tokenize():
    print(t)