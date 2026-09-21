import sys
with open('compiler/semantic/type_checker.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('and op != "+":', 'and op not in ["+", "==", "!=", "<", ">", "<=", ">="]:')

with open('compiler/semantic/type_checker.py', 'w', encoding='utf-8') as f:
    f.write(text)
