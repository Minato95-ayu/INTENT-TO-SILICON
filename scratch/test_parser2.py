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
for t in tokens:
    print(t.type, t.value)
