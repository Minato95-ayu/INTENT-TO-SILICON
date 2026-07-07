import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tests\test_phase74_package_manager.py'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Stripped BOM")
