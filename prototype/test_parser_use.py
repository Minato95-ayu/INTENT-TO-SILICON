import sys
sys.path.append('aayu_language')
from lexer import Lexer
from parser import Parser
tokens = Lexer('use auth.').tokenize()
print(tokens)
p = Parser(tokens)
print("Is KEYWORD use?", p.check("KEYWORD", "use"))
stmt = p.parse_statement()
print("Parsed:", stmt)
