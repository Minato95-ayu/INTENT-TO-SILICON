with open('src/self_hosted/lexer.aayu', 'r') as f:
    lines = f.readlines()

new_lines = []
in_tokenize = False
for line in lines:
    if 'action tokenize' in line:
        in_tokenize = True
    if line.strip() == 'end' and in_tokenize and len(line) - len(line.lstrip()) == 0:
        in_tokenize = False
    
    if in_tokenize and 'print(' in line:
        continue
    new_lines.append(line)

with open('src/self_hosted/lexer.aayu', 'w') as f:
    f.writelines(new_lines)
