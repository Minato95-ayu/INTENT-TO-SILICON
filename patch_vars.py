import re
with open('src/self_hosted/lexer.aayu', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove let from start_line, start_col, value inside the loops
text = re.sub(r'let\s+start_line\s*=\s*line', 'start_line = line', text)
text = re.sub(r'let\s+start_col\s*=\s*column', 'start_col = column', text)
text = re.sub(r'let\s+value\s*=\s*\"\"', 'value = ""', text)

# Insert the declaration at the top of the outer while loop
insert_pos = text.find('        # skip whitespace')
decl = '''        let start_line = 0
        let start_col = 0
        let value = ""
'''
text = text[:insert_pos] + decl + text[insert_pos:]

with open('src/self_hosted/lexer.aayu', 'w', encoding='utf-8') as f:
    f.write(text)
