with open('src/self_hosted/lexer.aayu', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('true', '1')
text = text.replace('false', '0')

with open('src/self_hosted/lexer.aayu', 'w', encoding='utf-8') as f:
    f.write(text)
