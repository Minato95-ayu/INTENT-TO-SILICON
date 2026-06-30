import os
import re

# 1. Update ast_nodes.py
ast_nodes_path = r"prototype\aayu_language\ast_nodes.py"
with open(ast_nodes_path, "r", encoding="utf-8") as f:
    ast_content = f.read()

unary_node = """
@dataclass
class UnaryExpressionNode(Node):
    operator: str
    right: Node
"""
if "UnaryExpressionNode" not in ast_content:
    ast_content = ast_content.replace("@dataclass\nclass BinaryExpressionNode", unary_node + "\n@dataclass\nclass BinaryExpressionNode")
    with open(ast_nodes_path, "w", encoding="utf-8") as f:
        f.write(ast_content)
    print("Updated ast_nodes.py")

# 2. Update ir.py
ir_path = r"prototype\aayu_language\ir.py"
with open(ir_path, "r", encoding="utf-8") as f:
    ir_content = f.read()

if "NEG = auto()" not in ir_content:
    ir_content = ir_content.replace("MOD = auto()", "MOD = auto()\n    NEG = auto()")
    with open(ir_path, "w", encoding="utf-8") as f:
        f.write(ir_content)
    print("Updated ir.py")

# 3. Update parser.py
parser_path = r"prototype\aayu_language\parser.py"
with open(parser_path, "r", encoding="utf-8") as f:
    parser_content = f.read()

if "UnaryExpressionNode" not in parser_content:
    parser_content = parser_content.replace("BinaryExpressionNode,", "BinaryExpressionNode, UnaryExpressionNode,")

# Add parse_unary
parse_unary_code = """
    def parse_unary(self) -> Node:
        if self.match("MINUS"):
            operator = self.previous().value
            right = self.parse_unary()
            return UnaryExpressionNode(operator=operator, right=right)
        return self.parse_primary()
"""
if "def parse_unary" not in parser_content:
    parser_content = parser_content.replace("def parse_factor(self) -> Node:", parse_unary_code + "\n    def parse_factor(self) -> Node:")

# Update parse_factor to call parse_unary
parser_content = parser_content.replace("expr = self.parse_primary()", "expr = self.parse_unary()")
parser_content = parser_content.replace("right = self.parse_primary()", "right = self.parse_unary()")

# Add parenthesis to parse_primary
paren_code = """        if self.match("LPAREN"):
            expr = self.parse_expression()
            self.consume("RPAREN", "Expect ')' after expression.")
            return expr
"""
if "self.match(\"LPAREN\"):" not in parser_content.split("def parse_primary")[1]:
    parser_content = parser_content.replace('if self.match("KEYWORD", "read"):', paren_code + '\n        if self.match("KEYWORD", "read"):')

with open(parser_path, "w", encoding="utf-8") as f:
    f.write(parser_content)
print("Updated parser.py")

# 4. Update compiler.py
compiler_path = r"prototype\aayu_language\compiler.py"
with open(compiler_path, "r", encoding="utf-8") as f:
    compiler_content = f.read()

if "UnaryExpressionNode" not in compiler_content:
    compiler_content = compiler_content.replace("BinaryExpressionNode,", "BinaryExpressionNode, UnaryExpressionNode,")

visit_unary = """
    def visit_UnaryExpressionNode(self, node: UnaryExpressionNode):
        self.visit(node.right)
        if node.operator in ('-', 'minus'):
            self._emit(Opcode.NEG)
"""
if "visit_UnaryExpressionNode" not in compiler_content:
    compiler_content = compiler_content.replace("    def visit_BinaryExpressionNode", visit_unary + "\n    def visit_BinaryExpressionNode")
    
# Update BinaryExpressionNode to handle MOD
if "Opcode.MOD" not in compiler_content:
    compiler_content = compiler_content.replace("self._emit(Opcode.DIV)", "self._emit(Opcode.DIV)\n        elif node.operator in ('modulo', '%', 'MOD'):\n            self._emit(Opcode.MOD)")

with open(compiler_path, "w", encoding="utf-8") as f:
    f.write(compiler_content)
print("Updated compiler.py")

