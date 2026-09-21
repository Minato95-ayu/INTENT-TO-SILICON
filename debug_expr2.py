import re

with open('compiler/parser/parser.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('f"Expect expression, got {token.type.name}"', 'f"Expect expression, got {token.type.name} at line {token.line}"')

with open('compiler/parser/parser.py', 'w', encoding='utf-8') as f:
    f.write(text)
