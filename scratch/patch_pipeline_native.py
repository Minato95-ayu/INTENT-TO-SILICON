import re

with open('compiler/ir/pipeline.py', 'r') as f:
    content = f.read()

old_code = '''            if "." in hir.name:
                mir_list.append(MIRInstruction("OP_ASYNC_CALL", [hir.name, len(hir.args)]))
            else:
                mir_list.append(MIRInstruction("CALL_ACTION", [hir.name]))'''

new_code = '''            if "." in hir.name or hir.name in ["print", "len", "type"]:
                mir_list.append(MIRInstruction("OP_ASYNC_CALL", [hir.name, len(hir.args)]))
            else:
                mir_list.append(MIRInstruction("CALL_ACTION", [hir.name]))'''

content = content.replace(old_code, new_code)

with open('compiler/ir/pipeline.py', 'w') as f:
    f.write(content)
