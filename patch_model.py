import re

with open('src/self_hosted/lexer.aayu', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('''model Token
    type
    value
    line
    column
end''', '''model Token {
    type String
    value String
    line Integer
    column Integer
}''')

text = text.replace('''model LexerState
    source
    pos
    line
    column
    length
end''', '''model LexerState {
    source String
    pos Integer
    line Integer
    column Integer
    length Integer
}''')

with open('src/self_hosted/lexer.aayu', 'w', encoding='utf-8') as f:
    f.write(text)
