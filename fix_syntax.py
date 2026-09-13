with open('compiler/semantic/type_inference.py', 'r') as f:
    lines = f.readlines()

out = []
for line in lines:
    if 'data_type = "Any"        elif isinstance(node, SemanticLetDeclNode):' in line:
        out.append('                data_type = "Any"\n')
        out.append('        elif isinstance(node, SemanticLetDeclNode):\n')
    else:
        out.append(line)

with open('compiler/semantic/type_inference.py', 'w') as f:
    f.writelines(out)
