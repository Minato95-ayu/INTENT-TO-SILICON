from typing import List
from compiler.semantic.nodes import (
    SemanticProgramNode, SemanticStateDeclNode, SemanticWidgetNode,
    SemanticLiteralNode, SemanticAssignmentNode, SemanticImportNode,
    SemanticActionDeclNode, SemanticActionCallNode, SemanticIdentifierNode
)
from compiler.ir.hir import (
    HIRNode, HIRStateDecl, HIRWidget, HIRAssignment,
    HIRActionDecl, HIRActionCall, HIRLoadVar, HIRPrint, HIRImport
)
from compiler.ir.mir import MIRNode, MIRInstruction
from compiler.ir.lir import LIRNode

class IRPipeline:
    """Three-stage IR lowering: Semantic AST → HIR → MIR → LIR"""

    # ── HIR Stage ──────────────────────────────────────────────

    def to_hir(self, semantic_ast: SemanticProgramNode) -> List[HIRNode]:
        hir_list = []
        for stmt in semantic_ast.statements:
            hir_node = self._semantic_to_hir(stmt)
            if hir_node is not None:
                hir_list.append(hir_node)
        return hir_list

    def _semantic_to_hir(self, node):
        if isinstance(node, SemanticStateDeclNode):
            value = node.value.value if isinstance(node.value, SemanticLiteralNode) else 0
            return HIRStateDecl(node.name, value)

        elif isinstance(node, SemanticWidgetNode):
            children_hir = []
            for child in node.children:
                child_hir = self._semantic_to_hir(child)
                if child_hir is not None:
                    children_hir.append(child_hir)
            return HIRWidget(node.widget_type, node.props, children_hir)

        elif isinstance(node, SemanticAssignmentNode):
            value = node.value.value if isinstance(node.value, SemanticLiteralNode) else 0
            return HIRAssignment(node.target, value)

        elif isinstance(node, SemanticActionDeclNode):
            body_hir = []
            for stmt in node.statements:
                h = self._semantic_to_hir(stmt)
                if h is not None:
                    body_hir.append(h)
            return HIRActionDecl(node.name, body_hir)

        elif isinstance(node, SemanticActionCallNode):
            return HIRActionCall(node.name, [])

        elif isinstance(node, SemanticIdentifierNode):
            return HIRLoadVar(node.name)

        elif isinstance(node, SemanticImportNode):
            return HIRImport(node.module)

        elif isinstance(node, SemanticLiteralNode):
            # Standalone literal (e.g. inside a widget child list)
            return HIRPrint(node.value)

        return None

    # ── MIR Stage ──────────────────────────────────────────────

    def to_mir(self, hir_list: List[HIRNode]) -> List[MIRNode]:
        mir_list = []
        for hir in hir_list:
            self._hir_to_mir(hir, mir_list)
        return mir_list

    def _hir_to_mir(self, hir, mir_list: list):
        if isinstance(hir, HIRStateDecl):
            mir_list.append(MIRInstruction("INIT_STATE", [hir.name, hir.value]))

        elif isinstance(hir, HIRWidget):
            # For text widgets whose children are variable references,
            # emit LOAD_VAR + PRINT directly (state-bound text)
            if hir.w_type.lower() == "text" and hir.children:
                for child in hir.children:
                    if isinstance(child, HIRLoadVar):
                        mir_list.append(MIRInstruction("LOAD_VAR", [child.name]))
                        mir_list.append(MIRInstruction("PRINT_STACK", []))
                    else:
                        self._hir_to_mir(child, mir_list)
                return
            
            # First recursively process children
            for child in hir.children:
                self._hir_to_mir(child, mir_list)
            # Then emit the widget itself
            mir_list.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [hir.props]))

        elif isinstance(hir, HIRAssignment):
            mir_list.append(MIRInstruction("SET_STATE", [hir.target, hir.value]))

        elif isinstance(hir, HIRActionDecl):
            body_mir = []
            for stmt in hir.body:
                self._hir_to_mir(stmt, body_mir)
            mir_list.append(MIRInstruction("ACTION_DECL", [hir.name, body_mir]))

        elif isinstance(hir, HIRActionCall):
            mir_list.append(MIRInstruction("CALL_ACTION", [hir.name]))

        elif isinstance(hir, HIRLoadVar):
            mir_list.append(MIRInstruction("LOAD_VAR", [hir.name]))

        elif isinstance(hir, HIRPrint):
            mir_list.append(MIRInstruction("PRINT", [hir.value]))

        elif isinstance(hir, HIRImport):
            # Imports are resolved at semantic stage; skip in IR
            pass

    # ── LIR Stage ──────────────────────────────────────────────

    def to_lir(self, mir_list: List[MIRNode]) -> List[LIRNode]:
        lir_list = []
        for mir in mir_list:
            self._mir_to_lir(mir, lir_list)
        return lir_list

    def _mir_to_lir(self, mir, lir_list: list):
        if not isinstance(mir, MIRInstruction):
            return

        if mir.opcode == "INIT_STATE":
            # INIT_STATE [name, value] → STATE_INIT [name, value]
            lir_list.append(LIRNode("STATE_INIT", [mir.operands[0], mir.operands[1]]))

        elif mir.opcode == "SET_STATE":
            # SET_STATE [name, value] → PUSH_CONST + STORE_VAR
            lir_list.append(LIRNode("PUSH_CONST", [mir.operands[1]]))
            lir_list.append(LIRNode("STORE_VAR", [mir.operands[0]]))

        elif mir.opcode.startswith("INIT_"):
            # INIT_TEXT, INIT_BUTTON, etc. → BUILD_*
            widget_type = mir.opcode[5:]  # strip "INIT_"
            lir_list.append(LIRNode(f"BUILD_{widget_type}", [mir.operands[0] if mir.operands else {}]))

        elif mir.opcode == "ACTION_DECL":
            # ACTION_DECL [name, body_mir_list]
            body_lir = []
            if len(mir.operands) > 1 and isinstance(mir.operands[1], list):
                for sub_mir in mir.operands[1]:
                    self._mir_to_lir(sub_mir, body_lir)
            lir_list.append(LIRNode("ACTION_DECL", [mir.operands[0], body_lir]))

        elif mir.opcode == "CALL_ACTION":
            lir_list.append(LIRNode("CALL_ACTION", [mir.operands[0]]))

        elif mir.opcode == "LOAD_VAR":
            lir_list.append(LIRNode("LOAD_VAR", [mir.operands[0]]))

        elif mir.opcode == "PRINT":
            lir_list.append(LIRNode("PRINT", [mir.operands[0]]))

        elif mir.opcode == "PRINT_STACK":
            # Value is already on the stack from a preceding LOAD_VAR
            lir_list.append(LIRNode("PRINT_STACK", []))
