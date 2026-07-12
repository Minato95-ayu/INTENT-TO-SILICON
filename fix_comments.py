import os
for root, dirs, files in os.walk('website'):
    for f in files:
        if f.endswith(('.ts', '.tsx')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as file:
                content = file.read()
            if content.startswith('/* eslint-disable */\n'):
                content = content[len('/* eslint-disable */\n'):]
                with open(p, 'w', encoding='utf-8') as file:
                    file.write(content)
