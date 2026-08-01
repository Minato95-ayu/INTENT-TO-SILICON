from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser

source = """
action main()
    notes.push("Hello")
end
"""

lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
print(ast)
