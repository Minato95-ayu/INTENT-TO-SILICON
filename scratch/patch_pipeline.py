import re

with open('compiler/ir/pipeline.py', 'r') as f:
    content = f.read()

# Fix semantic to hir
content = content.replace(
    'return HIRActionCall(node.name, [])',
    'arg_hirs = [self._semantic_to_hir(a) for a in getattr(node, \'args\', [])]\n            return HIRActionCall(node.name, arg_hirs)'
)

# Fix hir to mir
old_mir = 'elif isinstance(hir, HIRActionCall):\n            mir_list.append(MIRInstruction("CALL_ACTION", [hir.name]))'
new_mir = '''elif isinstance(hir, HIRActionCall):
            for arg in hir.args:
                self._hir_to_mir(arg, mir_list)
            if "." in hir.name:
                mir_list.append(MIRInstruction("OP_ASYNC_CALL", [hir.name, len(hir.args)]))
            else:
                mir_list.append(MIRInstruction("CALL_ACTION", [hir.name]))'''

content = content.replace(old_mir, new_mir)

with open('compiler/ir/pipeline.py', 'w') as f:
    f.write(content)
