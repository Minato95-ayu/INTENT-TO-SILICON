"""
=============================================================================
FILE: patch_blocknode.py
PURPOSE: Fixes or patches existing code
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles fixes or patches existing code.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import re

# 1. Update ast_nodes.py
ast_path = r"prototype\aayu_language\ast_nodes.py"
with open(ast_path, "r", encoding="utf-8") as f:
    ast_content = f.read()

if "class BlockNode(Node):" not in ast_content:
    block_node_code = """
@dataclass
class BlockNode(Node):
    statements: List[Node]
"""
    ast_content = ast_content.replace("@dataclass\nclass ProgramNode", block_node_code + "\n@dataclass\nclass ProgramNode")
    # Also add BlockNode to the export list if there is one (there isn't, but parser uses it, wait compiler will use it)
    with open(ast_path, "w", encoding="utf-8") as f:
        f.write(ast_content)

# 2. Update compiler.py
compiler_path = r"prototype\aayu_language\compiler.py"
with open(compiler_path, "r", encoding="utf-8") as f:
    compiler_content = f.read()

if "def visit_BlockNode" not in compiler_content:
    visit_block_code = """
    def visit_BlockNode(self, node: BlockNode):
        for stmt in node.statements:
            self.visit(stmt)
"""
    compiler_content = compiler_content.replace("    def visit_ProgramNode", visit_block_code + "\n    def visit_ProgramNode")
    
    # ensure it imports BlockNode
    compiler_content = compiler_content.replace("ProgramNode,", "BlockNode, ProgramNode,")
    with open(compiler_path, "w", encoding="utf-8") as f:
        f.write(compiler_content)

# 3. Update lowering.py
lowering_path = r"prototype\aayu_language\passes\lowering.py"
with open(lowering_path, "r", encoding="utf-8") as f:
    lowering_content = f.read()

# Change return types of visit_RepeatNode and visit_ForRangeNode from List[Node] to Node
lowering_content = lowering_content.replace("def visit_RepeatNode(self, node: RepeatNode) -> List[Node]:", "def visit_RepeatNode(self, node: RepeatNode) -> Node:")
lowering_content = lowering_content.replace("return [init, while_node]", "return BlockNode(statements=[init, while_node])")

lowering_content = lowering_content.replace("def visit_ForRangeNode(self, node: ForRangeNode) -> List[Node]:", "def visit_ForRangeNode(self, node: ForRangeNode) -> Node:")

with open(lowering_path, "w", encoding="utf-8") as f:
    f.write(lowering_content)

print("BlockNode added and Lowering Pass updated.")
