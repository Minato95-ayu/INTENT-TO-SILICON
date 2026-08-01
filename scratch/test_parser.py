from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser

source = '''
page ChatList
    column
        heading "AAYU WhatsApp Clone"
    end
end
'''

lexer = Lexer(source)
tokens = lexer.tokenize()
print([t.value for t in tokens])

parser = Parser(tokens)
ast = parser.parse()
print(ast)
