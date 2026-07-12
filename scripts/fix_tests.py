import os

init_file = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine\__init__.py'
with open(init_file, 'w', encoding='utf-8') as f:
    f.write('''''')

test_ie = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tests\test_intent_engine.py'
with open(test_ie, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('from offline_nlp import OfflineNLP', 'from intent_engine.offline_nlp import OfflineNLPEngine as OfflineNLP')

with open(test_ie, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed imports and syntax error")
