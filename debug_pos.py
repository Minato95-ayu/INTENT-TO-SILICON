with open('src/self_hosted/lexer.aayu', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('let loop = 1 == 1', 'let loop = 1 == 1\n    print("Starting loop!")')
text = text.replace('if pos >= length\n            print("Lexed token:")', 'print("pos is:"); print(pos)\n        if pos >= length\n            print("Lexed token:")')

with open('src/self_hosted/lexer.aayu', 'w', encoding='utf-8') as f:
    f.write(text)
