with open('compiler/ast/nodes.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'BinaryOpNode' not in content:
    binary_op_node = '''
@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode
    def __post_init__(self):
        super().__init__(self.line, self.column)
'''
    content += binary_op_node

with open('compiler/ast/nodes.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('compiler/parser/parser.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

if 'def _parse_term' not in content:
    new_expr = '''    def _parse_expression(self):
        return self._parse_term()

    def _parse_term(self):
        expr = self._parse_factor()
        while self._match(TokenType.OPERATOR, "+") or self._match(TokenType.OPERATOR, "-"):
            operator = self._previous().value
            right = self._parse_factor()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr

    def _parse_factor(self):
        expr = self._parse_primary()
        while self._match(TokenType.OPERATOR, "*") or self._match(TokenType.OPERATOR, "/"):
            operator = self._previous().value
            right = self._parse_primary()
            from aayu.compiler.ast.nodes import BinaryOpNode
            expr = BinaryOpNode(line=expr.line, column=expr.column, left=expr, operator=operator, right=right)
        return expr

    def _parse_primary(self):'''
    
    old_expr = '''    def _parse_expression(self):'''
    content = content.replace(old_expr, new_expr)
    
    with open('compiler/parser/parser.py', 'w', encoding='utf-8') as f:
        f.write(content)

with open('compiler/semantic/nodes.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'SemanticBinaryOpNode' not in content:
    node = '''
@dataclass
class SemanticBinaryOpNode(SemanticNode):
    left: SemanticNode
    op: str
    right: SemanticNode
'''
    content += node
    with open('compiler/semantic/nodes.py', 'w', encoding='utf-8') as f:
        f.write(content)

with open('compiler/semantic/analyzer.py', 'r', encoding='utf-8') as f:
    content = f.read()

if '_visit_BinaryOpNode' not in content:
    visit_code = '''
    def _visit_BinaryOpNode(self, node) -> SemanticNode:
        left = self._visit_node(node.left)
        right = self._visit_node(node.right)
        from aayu.compiler.semantic.nodes import SemanticBinaryOpNode
        return SemanticBinaryOpNode(line=node.line, column=node.column, left=left, op=node.operator, right=right)

    def _visit_LiteralNode'''
    content = content.replace('    def _visit_LiteralNode', visit_code)
    with open('compiler/semantic/analyzer.py', 'w', encoding='utf-8') as f:
        f.write(content)

with open('compiler/ir/hir.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'HIRBinaryOp' not in content:
    hir_node = '''
@dataclass(frozen=True)
class HIRBinaryOp(HIRNode):
    left: HIRNode
    op: str
    right: HIRNode
'''
    content += hir_node
    with open('compiler/ir/hir.py', 'w', encoding='utf-8') as f:
        f.write(content)

with open('compiler/ir/pipeline.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'SemanticBinaryOpNode' not in content:
    content = content.replace(
        'elif isinstance(node, SemanticLiteralNode):',
        '''elif type(node).__name__ == "SemanticBinaryOpNode":
            from aayu.compiler.ir.hir import HIRBinaryOp
            return HIRBinaryOp(self._semantic_to_hir(node.left), node.op, self._semantic_to_hir(node.right))
        elif isinstance(node, SemanticLiteralNode):'''
    )
    
    content = content.replace(
        'elif isinstance(hir, HIRLiteral):',
        '''elif type(hir).__name__ == "HIRBinaryOp":
            self._hir_to_mir(hir.left, mir_list)
            self._hir_to_mir(hir.right, mir_list)
            if hir.op == "+":
                mir_list.append(MIRInstruction("ADD", []))
            elif hir.op == "-":
                mir_list.append(MIRInstruction("SUB", []))
            elif hir.op == "*":
                mir_list.append(MIRInstruction("MUL", []))
            elif hir.op == "/":
                mir_list.append(MIRInstruction("DIV", []))
        elif isinstance(hir, HIRLiteral):'''
    )
    with open('compiler/ir/pipeline.py', 'w', encoding='utf-8') as f:
        f.write(content)

