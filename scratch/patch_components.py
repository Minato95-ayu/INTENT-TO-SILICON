
import os

pipeline_path = "compiler/ir/pipeline.py"
with open(pipeline_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace _hir_to_mir logic for page
old_page_logic = """
            if hir.w_type.lower() == "page":
                mir_list.append(MIRInstruction("MARK_PAGE_START", []))
                
            is_block = hir.w_type.lower() in ["page", "container", "row", "column", "card"]
            if is_block:
                mir_list.append(MIRInstruction("MARK_BLOCK_START", []))
                
            # First recursively process children
            for child in hir.children:
                self._hir_to_mir(child, mir_list)
            # Then emit the widget itself
            mir_list.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [hir.props]))
"""

new_page_logic = """
            if hir.w_type.lower() == "page":
                page_name = hir.props.get("name", "")
                
                # Main App page gets MARK_PAGE_START
                if page_name == "App":
                    mir_list.append(MIRInstruction("MARK_PAGE_START", []))
                    mir_list.append(MIRInstruction("MARK_BLOCK_START", []))
                    for child in hir.children:
                        self._hir_to_mir(child, mir_list)
                    mir_list.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [hir.props]))
                else:
                    # Components are compiled as actions!
                    body_mir = []
                    body_mir.append(MIRInstruction("MARK_BLOCK_START", []))
                    for child in hir.children:
                        self._hir_to_mir(child, body_mir)
                    body_mir.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [hir.props]))
                    mir_list.append(MIRInstruction("ACTION_DECL", [page_name, body_mir]))
            elif hir.w_type.lower() == "call":
                # calling a component is calling its action
                target = hir.props.get("target", "")
                mir_list.append(MIRInstruction("CALL_ACTION", [target]))
            else:
                is_block = hir.w_type.lower() in ["container", "row", "column", "card"]
                if is_block:
                    mir_list.append(MIRInstruction("MARK_BLOCK_START", []))
                    
                # First recursively process children
                for child in hir.children:
                    self._hir_to_mir(child, mir_list)
                # Then emit the widget itself
                mir_list.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [hir.props]))
"""

content = content.replace(old_page_logic, new_page_logic)

with open(pipeline_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patched pipeline.py!")

