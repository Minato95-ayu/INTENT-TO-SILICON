with open('src/self_hosted/lexer.aayu', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('type String', 'type: String')
text = text.replace('value String', 'value: String')
text = text.replace('line Integer', 'line: Integer')
text = text.replace('column Integer', 'column: Integer')
text = text.replace('source String', 'source: String')
text = text.replace('pos Integer', 'pos: Integer')
text = text.replace('length Integer', 'length: Integer')

with open('src/self_hosted/lexer.aayu', 'w', encoding='utf-8') as f:
    f.write(text)
