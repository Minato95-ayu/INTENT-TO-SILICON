import re

with open('compiler/ir/pipeline.py', 'r') as f:
    content = f.read()

content = content.replace('lir_list.append(LIRNode("OP_ASYNC_CALL", []))', 'lir_list.append(LIRNode("OP_ASYNC_CALL", [mir.operands[0], mir.operands[1]]))')

with open('compiler/ir/pipeline.py', 'w') as f:
    f.write(content)
