import os

def enable_eslint(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('/* eslint-disable */\n'):
        content = content[len('/* eslint-disable */\n'):]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

for root, dirs, files in os.walk('website'):
    if '.next' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.tsx') or f.endswith('.ts'):
            enable_eslint(os.path.join(root, f))
