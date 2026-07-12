from typing import List
from compiler.semantic.nodes import SemanticProgramNode, SemanticStateDeclNode, SemanticWidgetNode, SemanticLiteralNode
from compiler.ir.hir import HIRNode, HIRStateDecl, HIRWidget
from compiler.ir.mir import MIRNode, MIRInstruction
from compiler.ir.lir import LIRNode

class IRPipeline:
    def to_hir(self, semantic_ast: SemanticProgramNode) -> List[HIRNode]:
        hir_list = []
        for stmt in semantic_ast.statements:
            if isinstance(stmt, SemanticStateDeclNode):
                hir_list.append(HIRStateDecl(stmt.name, stmt.value.value))
            elif isinstance(stmt, SemanticWidgetNode):
                # We would recursively build HIRWidget here
                hir_list.append(HIRWidget(stmt.widget_type, stmt.props, []))
        return hir_list

    def to_mir(self, hir_list: List[HIRNode]) -> List[MIRNode]:
        mir_list = []
        for hir in hir_list:
            if isinstance(hir, HIRStateDecl):
                mir_list.append(MIRInstruction("INIT_STATE", [hir.name, hir.value]))
            elif isinstance(hir, HIRWidget):
                mir_list.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [hir.props]))
        return mir_list

    def to_lir(self, mir_list: List[MIRNode]) -> List[LIRNode]:
        lir_list = []
        for mir in mir_list:
            if mir.opcode == "INIT_STATE":
                lir_list.append(LIRNode("STATE_INIT", [mir.operands[0], mir.operands[1]]))
            elif mir.opcode.startswith("INIT_"):
                # Map to BUILD_* bytecode
                lir_list.append(LIRNode(f"BUILD_{mir.opcode[5:]}", [mir.operands[0]]))
        return lir_list
