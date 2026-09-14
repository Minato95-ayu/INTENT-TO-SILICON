import re

with open("compiler/lexer/tokens.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('"if", "else",', '"if", "elif", "else",')

with open("compiler/lexer/tokens.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Added elif to keywords")
