import re

with open('compiler/ir/pipeline.py', 'r') as f:
    content = f.read()

content = content.replace('elif mir.opcode == "ASYNC_CALL":', 'elif mir.opcode == "OP_ASYNC_CALL":')

with open('compiler/ir/pipeline.py', 'w') as f:
    f.write(content)
