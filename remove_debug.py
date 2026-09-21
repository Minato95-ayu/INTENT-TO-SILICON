import re

with open('compiler/ir/pipeline.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'\s*print\(f"\[DEBUG HIR\] BinaryOp left=\{type\(hir\.left\)\} right=\{type\(hir\.right\)\}"\)', '', text)

with open('compiler/ir/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(text)
