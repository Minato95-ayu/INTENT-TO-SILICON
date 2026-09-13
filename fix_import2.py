with open('compiler/semantic/type_checker.py', 'r') as f:
    content = f.read()

content = content.replace("SemanticModelNode", "SemanticModelDeclNode")

with open('compiler/semantic/type_checker.py', 'w') as f:
    f.write(content)
