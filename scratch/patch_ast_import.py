# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import re

with open('compiler/ast/nodes.py', 'r') as f:
    content = f.read()

import_node = """
@dataclass(frozen=True)
class ImportNode(ASTNode):
    module: str
"""

if "class ImportNode" not in content:
    content += "\n" + import_node

with open('compiler/ast/nodes.py', 'w') as f:
    f.write(content)
print("Updated nodes.py")
