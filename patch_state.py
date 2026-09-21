with open('src/self_hosted/lexer.aayu', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('state.', 'st.')
text = text.replace('state)', 'st)')
text = text.replace('state)', 'st)')
text = text.replace('(state', '(st')
text = text.replace('let state', 'let st')

with open('src/self_hosted/lexer.aayu', 'w', encoding='utf-8') as f:
    f.write(text)
