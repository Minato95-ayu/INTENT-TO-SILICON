import os, re

def fix_lint(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r':\s*any\b', ': unknown', content)

    content = content.replace('// Internal State Simulation', '{/* Internal State Simulation */}')
    content = content.replace('// AAYU Compiler passes', '{/* AAYU Compiler passes */}')
    content = content.replace('// Execution output will appear here', '{/* Execution output will appear here */}')

    content = content.replace("AAYU's", "AAYU&apos;s")
    content = content.replace("doesn't", "doesn&apos;t")
    content = content.replace("Doesn't", "Doesn&apos;t")
    content = content.replace("don't", "don&apos;t")
    content = content.replace("Don't", "Don&apos;t")
    content = content.replace('System "Ready" state', 'System &quot;Ready&quot; state')
    content = content.replace('Type "/" to search', 'Type &quot;/&quot; to search')
    content = content.replace('game."', 'game.&quot;')
    content = content.replace('"That', '&quot;That')
    content = content.replace("world's", "world&apos;s")
    content = content.replace('\"intent\"', '&quot;intent&quot;')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('website'):
    if '.next' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.tsx') or f.endswith('.ts'):
            fix_lint(os.path.join(root, f))
