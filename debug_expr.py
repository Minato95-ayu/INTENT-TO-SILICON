import re

with open('compiler/parser/parser.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"Expect expression."', 'f"Expect expression. Line: {self._peek().line}"')

with open('compiler/parser/parser.py', 'w', encoding='utf-8') as f:
    f.write(text)
