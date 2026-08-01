from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser

l = Lexer('page App\ncontainer\nheading "AAYU WhatsApp Clone"\nend\nend\n')
tokens = l.tokenize()
for t in tokens:
    print(t.type, t.value)
    
p = Parser(tokens)
print(p.parse())
