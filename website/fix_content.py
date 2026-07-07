import os

path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\data\language-content.tsx'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the aayu.mod string
text = text.replace('{// aayu.mod\nmodule my_app 1.0.0\nrequire http_server >= 2.1.0}', '// aayu.mod\nmodule my_app 1.0.0\nrequire http_server >= 2.1.0')

# Fix node_modules
text = text.replace('massive \n ode_modules.', 'massive node_modules.')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

