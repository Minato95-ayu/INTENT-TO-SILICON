with open('src/self_hosted/lexer.aayu', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('let type = ', 'let tok_type = ')
text = text.replace('type = "KEYWORD"', 'tok_type = "KEYWORD"')
text = text.replace('type: type', 'type: tok_type')

with open('src/self_hosted/lexer.aayu', 'w', encoding='utf-8') as f:
    f.write(text)
