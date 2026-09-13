import re
with open('compiler/semantic/type_inference.py', 'r') as f:
    content = f.read()

replacement = """        elif isinstance(node, SemanticLetDeclNode):"""

content = re.sub(r'\s*elif isinstance\(node, SemanticLetDeclNode\):', replacement, content, count=1)

with open('compiler/semantic/type_inference.py', 'w') as f:
    f.write(content)
