import re

with open('compiler/parser/parser.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"Expect variable name after \'let\'."', '"Expect variable name after \'let\'. Line: " + str(self._previous().line)')

with open('compiler/parser/parser.py', 'w', encoding='utf-8') as f:
    f.write(text)
