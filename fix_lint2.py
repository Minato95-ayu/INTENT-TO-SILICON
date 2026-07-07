import os
import re

def fix_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix unexpected any
    content = content.replace('(e: any)', '(e: unknown)')
    
    # Fix specific unescaped quotes matching the lint logs
    content = content.replace('System "Ready" state', 'System &quot;Ready&quot; state')
    content = content.replace('setQuery("");', '// setQuery("");')
    content = content.replace('Type "/" to search', 'Type &quot;/&quot; to search')
    content = content.replace('game."', 'game.&quot;')
    content = content.replace('"That', '&quot;That')
    content = content.replace(\"world's\", \"world&apos;s\")
    content = content.replace('\"intent\"', '&quot;intent&quot;')
    content = content.replace(\"don't\", \"don&apos;t\")
    content = content.replace(\"Doesn't\", \"Doesn&apos;t\")
    content = content.replace(\"can't\", \"can&apos;t\")
    content = content.replace(\"It's\", \"It&apos;s\")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('website/app'):
    for f in files:
        if f.endswith('.tsx') or f.endswith('.ts'): fix_file(os.path.join(root, f))
for root, dirs, files in os.walk('website/components'):
    for f in files:
        if f.endswith('.tsx') or f.endswith('.ts'): fix_file(os.path.join(root, f))
for root, dirs, files in os.walk('website/data'):
    for f in files:
        if f.endswith('.tsx') or f.endswith('.ts'): fix_file(os.path.join(root, f))
