import ast
with open('compiler/parser/parser.py') as f:
    text = f.read()
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'def _parse_primary' in line:
        for j in range(i+60, i+100):
            print(lines[j])
        break
