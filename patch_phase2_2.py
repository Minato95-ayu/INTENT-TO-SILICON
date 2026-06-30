import os
import re

# 1. Update ir.py
ir_path = r"prototype\aayu_language\ir.py"
with open(ir_path, "r", encoding="utf-8") as f:
    ir_content = f.read()

ir_content = ir_content.replace("NOT_EQ = auto()", "NE = auto()")
ir_content = ir_content.replace("LTE = auto()", "LE = auto()")
ir_content = ir_content.replace("GTE = auto()", "GE = auto()")
with open(ir_path, "w", encoding="utf-8") as f:
    f.write(ir_content)
print("Updated ir.py")

# 2. Update lexer.py
lexer_path = r"prototype\aayu_language\lexer.py"
with open(lexer_path, "r", encoding="utf-8") as f:
    lexer_content = f.read()

# Add <=, >=, !=
if "LTE" not in lexer_content:
    repl = """            ("EQ_EQ", r'=='),
            ("NOT_EQ", r'!='),
            ("GTE", r'>='),
            ("LTE", r'<='),"""
    lexer_content = lexer_content.replace('            ("EQ_EQ", r\'==\'),', repl)
    with open(lexer_path, "w", encoding="utf-8") as f:
        f.write(lexer_content)
    print("Updated lexer.py")


# 3. Update ast_nodes.py
ast_path = r"prototype\aayu_language\ast_nodes.py"
with open(ast_path, "r", encoding="utf-8") as f:
    ast_content = f.read()

if "LogicalExpressionNode" not in ast_content:
    logic_node = """
@dataclass
class LogicalExpressionNode(Node):
    left: Node
    operator: str
    right: Node
"""
    ast_content = ast_content.replace("@dataclass\nclass UnaryExpressionNode", logic_node + "\n@dataclass\nclass UnaryExpressionNode")
    with open(ast_path, "w", encoding="utf-8") as f:
        f.write(ast_content)
    print("Updated ast_nodes.py")


# 4. Update parser.py
parser_path = r"prototype\aayu_language\parser.py"
with open(parser_path, "r", encoding="utf-8") as f:
    parser_content = f.read()

if "LogicalExpressionNode" not in parser_content:
    parser_content = parser_content.replace("UnaryExpressionNode,", "UnaryExpressionNode, LogicalExpressionNode,")

# Add parse_logical_or and parse_logical_and
# Precedence: parse_expression -> parse_logical_or -> parse_logical_and -> parse_comparison -> parse_term
if "def parse_logical_or" not in parser_content:
    logic_parse = """
    def parse_logical_or(self) -> Node:
        expr = self.parse_logical_and()
        while self.match("KEYWORD", "or"):
            operator = "or"
            right = self.parse_logical_and()
            expr = LogicalExpressionNode(left=expr, operator=operator, right=right)
        return expr

    def parse_logical_and(self) -> Node:
        expr = self.parse_comparison()
        while self.match("KEYWORD", "and"):
            operator = "and"
            right = self.parse_comparison()
            expr = LogicalExpressionNode(left=expr, operator=operator, right=right)
        return expr
"""
    parser_content = parser_content.replace("    def parse_comparison(self) -> Node:", logic_parse + "\n    def parse_comparison(self) -> Node:")
    # Update parse_expression to call parse_logical_or instead of parse_comparison
    parser_content = parser_content.replace("return self.parse_comparison()", "return self.parse_logical_or()")
    
    # Update parse_unary to handle 'not'
    not_unary = """        if self.match("KEYWORD", "not"):
            operator = "not"
            right = self.parse_unary()
            return UnaryExpressionNode(operator=operator, right=right)
"""
    parser_content = parser_content.replace("if self.match(\"MINUS\"):", not_unary + "        if self.match(\"MINUS\"):")
    
    # Add !=, <=, >= to parse_comparison
    # Currently it has:
    #         elif self.match("EQ_EQ"):
    #            operator = "=="
    #         elif self.match("GREATER"):
    comparisons = """        elif self.match("EQ_EQ"):
            operator = "=="
        elif self.match("NOT_EQ"):
            operator = "!="
        elif self.match("GTE"):
            operator = ">="
        elif self.match("LTE"):
            operator = "<="
        elif self.match("GREATER"):"""
    parser_content = re.sub(r'\s*elif self\.match\("EQ_EQ"\):\s*operator = "=="\s*elif self\.match\("GREATER"\):', comparisons, parser_content, count=1)
    
    with open(parser_path, "w", encoding="utf-8") as f:
        f.write(parser_content)
    print("Updated parser.py")


# 5. Update compiler.py
compiler_path = r"prototype\aayu_language\compiler.py"
with open(compiler_path, "r", encoding="utf-8") as f:
    compiler_content = f.read()

if "LogicalExpressionNode" not in compiler_content:
    compiler_content = compiler_content.replace("UnaryExpressionNode,", "UnaryExpressionNode, LogicalExpressionNode,")

if "def visit_LogicalExpressionNode" not in compiler_content:
    visit_logic = """
    def visit_LogicalExpressionNode(self, node: LogicalExpressionNode):
        self.visit(node.left)
        if node.operator == "and":
            jump_idx = self._emit(Opcode.JUMP_IF_FALSE, 0)
            # Pop left operand if true, to evaluate right operand
            self._emit(Opcode.POP)
            self.visit(node.right)
            # Patch jump
            self.bytecode.instructions[jump_idx].operand = len(self.bytecode.instructions) - jump_idx - 1
        elif node.operator == "or":
            jump_idx = self._emit(Opcode.JUMP_IF_TRUE, 0) # Need JUMP_IF_TRUE opcode
            self._emit(Opcode.POP)
            self.visit(node.right)
            self.bytecode.instructions[jump_idx].operand = len(self.bytecode.instructions) - jump_idx - 1
"""
    # Wait, we need JUMP_IF_TRUE. If not present, we can implement it by NOT + JUMP_IF_FALSE or just add JUMP_IF_TRUE.
    # Let's add JUMP_IF_TRUE to ir.py and compiler!
    compiler_content = compiler_content.replace("    def visit_BinaryExpressionNode", visit_logic + "\n    def visit_BinaryExpressionNode")
    
    # Update BinaryExpressionNode for comparisons
    bin_ops = """        elif node.operator == "==":
            self._emit(Opcode.EQ)
        elif node.operator == "!=":
            self._emit(Opcode.NE)
        elif node.operator == "<":
            self._emit(Opcode.LT)
        elif node.operator == ">":
            self._emit(Opcode.GT)
        elif node.operator == "<=":
            self._emit(Opcode.LE)
        elif node.operator == ">=":
            self._emit(Opcode.GE)"""
    # Replace existing ones
    compiler_content = re.sub(r'\s*elif node\.operator == "==":\s*self\._emit\(Opcode\.EQ\)\s*elif node\.operator == "<":\s*self\._emit\(Opcode\.LT\)\s*elif node\.operator == ">":\s*self\._emit\(Opcode\.GT\)', bin_ops, compiler_content, count=1)

    # Update visit_UnaryExpressionNode for not
    compiler_content = compiler_content.replace("if node.operator in ('-', 'minus'):", "if node.operator in ('-', 'minus'):\n            self._emit(Opcode.NEG)\n        elif node.operator == 'not':\n            self._emit(Opcode.NOT)\n        # Skip")

    with open(compiler_path, "w", encoding="utf-8") as f:
        f.write(compiler_content)
    print("Updated compiler.py")

# Update ir.py for JUMP_IF_TRUE
with open(ir_path, "r", encoding="utf-8") as f:
    ir_content = f.read()
if "JUMP_IF_TRUE = auto()" not in ir_content:
    ir_content = ir_content.replace("JUMP_IF_FALSE = auto()", "JUMP_IF_FALSE = auto()\n    JUMP_IF_TRUE = auto()")
    with open(ir_path, "w", encoding="utf-8") as f:
        f.write(ir_content)
    print("Updated ir.py for JUMP_IF_TRUE")

