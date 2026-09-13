with open('compiler/semantic/type_inference.py', 'r') as f:
    content = f.read()

replacement = """        elif isinstance(node, SemanticLetDeclNode):
            val_type = self._infer_node(node.value)
            sym = node.scope.resolve(node.name)
            if sym:
                sym.data_type = "Any" if val_type == "Null" else val_type
            data_type = "Void"
        elif isinstance(node, SemanticStateDeclNode):
            val_type = self._infer_node(node.value)
            sym = node.scope.resolve(node.name)
            if sym:
                sym.data_type = "Any" if val_type == "Null" else val_type
            data_type = "Void\""""

import re
content = re.sub(r'elif isinstance\(node, SemanticLetDeclNode\):.*?data_type = "Void"', replacement, content, flags=re.DOTALL)

with open('compiler/semantic/type_inference.py', 'w') as f:
    f.write(content)
