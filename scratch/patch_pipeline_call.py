
import os

pipeline_path = "compiler/ir/pipeline.py"
with open(pipeline_path, "r", encoding="utf-8") as f:
    content = f.read()

old_code = """            elif hir.w_type.lower() == "call":
                # calling a component is calling its action
                target = hir.props.get("target", "")
                mir_list.append(MIRInstruction("CALL_ACTION", [target]))"""

new_code = """            elif hir.w_type.lower() == "call":
                # calling a component is calling its action
                target = hir.props.get("target", "")
                if not target and hir.children:
                    # In parser, `call Navbar` puts Identifier("Navbar") as a child
                    first_child = hir.children[0]
                    if hasattr(first_child, "name"):
                        target = first_child.name
                mir_list.append(MIRInstruction("CALL_ACTION", [target]))"""

content = content.replace(old_code, new_code)

with open(pipeline_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Patched pipeline.py")

