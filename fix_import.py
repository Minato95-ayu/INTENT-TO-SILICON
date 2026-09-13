with open('compiler/semantic/type_inference.py', 'r') as f:
    content = f.read()

content = content.replace("SemanticModelNode", "SemanticModelDeclNode")

with open('compiler/semantic/type_inference.py', 'w') as f:
    f.write(content)
