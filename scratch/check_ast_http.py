import sys, os
sys.path.insert(0, os.path.abspath('.'))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser

source = '''
action main()
    data = HTTP.post("https://httpbin.org/post", {name: "AAYU", goal: "Intent-to-Silicon"})
    print(data)
end
'''
tokens = Lexer(source).tokenize()
ast = Parser(tokens).parse()
print(ast)
