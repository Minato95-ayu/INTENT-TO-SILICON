import re

with open('compiler/ir/pipeline.py', 'r') as f:
    content = f.read()

old_code = '''        elif isinstance(node, SemanticActionCallNode):
            arg_hirs = [self._semantic_to_hir(a) for a in getattr(node, 'args', [])]
            return HIRActionCall(node.name, arg_hirs)'''

new_code = '''        elif isinstance(node, SemanticActionCallNode):
            arg_hirs = []
            for a in getattr(node, 'args', []):
                h = self._semantic_to_hir(a)
                if isinstance(h, HIRPrint):
                    h = HIRLoadConst(h.value)
                arg_hirs.append(h)
            return HIRActionCall(node.name, arg_hirs)'''

content = content.replace(old_code, new_code)

with open('compiler/ir/pipeline.py', 'w') as f:
    f.write(content)
