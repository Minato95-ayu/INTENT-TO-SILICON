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

with open('compiler/parser/parser.py', 'r') as f:
    content = f.read()

# Add ImportNode to ast.nodes import
content = content.replace(
    'WidgetNode',
    'WidgetNode,\n    ImportNode'
)

# Parse import statement
parse_import = """
    def _parse_import_statement(self):
        line, col = self._previous().line, self._previous().column
        
        module_token = self._consume(TokenType.IDENTIFIER, "Expect module name after 'import'.")
        
        return ImportNode(line=line, column=col, module=module_token.value)
"""

if "_parse_import_statement" not in content:
    content = content.replace(
        'def _parse_state_declaration(self):',
        parse_import.strip() + '\n\n    def _parse_state_declaration(self):'
    )

# Hook it up in _parse_statement
if 'self._match(TokenType.KEYWORD, "import")' not in content:
    content = content.replace(
        'if self._match(TokenType.KEYWORD, "state"):',
        'if self._match(TokenType.KEYWORD, "import"):\n            return self._parse_import_statement()\n        \n        if self._match(TokenType.KEYWORD, "state"):'
    )

with open('compiler/parser/parser.py', 'w') as f:
    f.write(content)
print("Updated parser.py with import")
