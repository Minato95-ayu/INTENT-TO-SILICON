import re

with open('compiler/semantic/analyzer.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"file.read"', '"file::read"')
text = text.replace('"file.write"', '"file::write"')
text = text.replace('"file.append"', '"file::append"')
text = text.replace('"file.delete"', '"file::delete"')
text = text.replace('"file.exists"', '"file::exists"')
text = text.replace('"file.mkdir"', '"file::mkdir"')

with open('compiler/semantic/analyzer.py', 'w', encoding='utf-8') as f:
    f.write(text)
