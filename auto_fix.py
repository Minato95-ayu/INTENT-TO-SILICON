import json
import os
import re

with open('website/eslint_report.json', 'r', encoding='utf-16') as f:
    data = json.load(f)

for file_data in data:
    msgs = file_data.get('messages', [])
    if not msgs: continue
    path = file_data['filePath']
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')

    for msg in sorted(msgs, key=lambda x: (x['line'], x['column']), reverse=True):
        l = msg['line'] - 1
        c = msg['column'] - 1
        rule = msg['ruleId']
        if rule == 'react/no-unescaped-entities':
            char = lines[l][c:c+1]
            if char == "'": lines[l] = lines[l][:c] + '&apos;' + lines[l][c+1:]
            elif char == '"': lines[l] = lines[l][:c] + '&quot;' + lines[l][c+1:]
            elif char == '>': lines[l] = lines[l].replace("'", "&apos;").replace('"', "&quot;")
            else:
                lines[l] = lines[l].replace("'", "&apos;").replace('"', "&quot;")
        elif rule == 'react/jsx-no-comment-textnodes':
            lines[l] = lines[l].replace('//', '{/*') + ' */}'
        elif rule == '@typescript-eslint/no-explicit-any':
            lines[l] = lines[l][:c] + lines[l][c:].replace('any', 'unknown', 1)
        elif rule == '@typescript-eslint/no-unused-vars':
            var_name = re.search(r"'([^']+)' is defined but never used", msg['message'])
            if var_name:
                v = var_name.group(1)
                lines[l] = re.sub(r'\b' + v + r'\b\s*,?', '', lines[l])
                lines[l] = re.sub(r',\s*\}', ' }', lines[l])
                lines[l] = re.sub(r'\{\s*\}', '', lines[l])
                if 'import  from' in lines[l] or 'import from' in lines[l]:
                    lines[l] = ''

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
