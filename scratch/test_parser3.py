from aayu.compiler.lexer.lexer import Lexer
source = '''
column
    text "Hello"
end
'''
lexer = Lexer(source)
for t in lexer.tokenize():
    print(t.type, t.value)
