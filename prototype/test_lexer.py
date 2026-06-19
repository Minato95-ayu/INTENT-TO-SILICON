import sys
sys.path.append('aayu_language')
from lexer import Lexer
print(Lexer('use auth.').tokenize())
