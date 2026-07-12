import os
import re

path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any occurrence of the corrupted string
text = re.sub(r'className=\{.*?ransition-opacity duration-500.*?\}', 'className="transition-opacity duration-500"', text)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Fixed JSX classes in page.tsx")
