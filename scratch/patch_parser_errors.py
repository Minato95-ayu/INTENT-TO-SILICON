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

# Replace ParserError definition
content = re.sub(
    r'class ParserError\(Exception\):\n\s+pass',
    'from compiler.errors import CompilerError\n\n# Deprecated, using CompilerError directly\nclass ParserError(CompilerError):\n    pass',
    content
)

# Replace raise ParserError(f"Unexpected token {token.value} at line {token.line}")
content = content.replace(
    'raise ParserError(f"Unexpected token {token.value} at line {token.line}")',
    'raise CompilerError(f"Unexpected token \'{token.value}\'", token.line, token.column, token.source_line)'
)

# Replace raise ParserError(f"Expect expression, got {token.type} at line {token.line}")
content = content.replace(
    'raise ParserError(f"Expect expression, got {token.type} at line {token.line}")',
    'raise CompilerError(f"Expect expression, got {token.type.name}", token.line, token.column, token.source_line)'
)

# Replace raise ParserError(f"{message} at line {self._peek().line}")
content = content.replace(
    'raise ParserError(f"{message} at line {self._peek().line}")',
    'peek = self._peek()\n        raise CompilerError(message, peek.line, peek.column, peek.source_line)'
)

with open('compiler/parser/parser.py', 'w') as f:
    f.write(content)
print("Updated parser.py")
