import os

linearizer_path = 'compiler/ir/linearizer.py'
with open(linearizer_path, 'r', encoding='utf-8') as f:
    lin = f.read()

# Let's check if SubscriptNode is imported and handled.
if 'SubscriptNode' not in lin:
    print('SubscriptNode not in linearizer')
else:
    print('SubscriptNode is present')

