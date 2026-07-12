import os
path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any occurrence of the corrupted string
text = text.replace('className={\t' + 'ransition-opacity duration-500 \\}', 'className="transition-opacity duration-500"')
# Or maybe there is no backslash just }
import re
text = re.sub(r'className=\{.*?ransition-opacity duration-500.*?\}', 'className="transition-opacity duration-500"', text)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
