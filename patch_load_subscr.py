import re

with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('val = container[index]', 'val = container[index]\n        print("LOAD_SUBSCR:", type(container), container, type(index), index, "->", val)')

with open('runtime/vm/interpreter.py', 'w', encoding='utf-8') as f:
    f.write(text)
