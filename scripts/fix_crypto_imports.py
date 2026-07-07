import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules\crypto_lib.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('from ...values.null import NullValue', 'from ...values.null import NullValue\nfrom ...values.boolean import BooleanValue')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added BooleanValue import")
