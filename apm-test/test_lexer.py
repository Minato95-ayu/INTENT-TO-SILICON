import sys
sys.path.append('../prototype/aayu_language')
from lexer import Lexer
print([(t.type, t.value) for t in Lexer('return "Status: " + res.status + ", Title: " + res.body.title.').tokenize()])
