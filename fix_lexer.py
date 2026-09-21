import sys

with open('src/self_hosted/lexer.aayu', 'r') as f:
    code = f.read()

# Remove model Token
import re
code = re.sub(r'model Token \{\s*type: String\s*value: String\s*line: Integer\s*column: Integer\s*\}', '', code)

# Replace Token(type, value, line, col) with dictionary
code = re.sub(r'Token\(([^,]+),\s*([^,]+),\s*([^,]+),\s*([^\)]+)\)', r'{ "type": \1, "value": \2, "line": \3, "column": \4 }', code)

# Fix t.type and t.value
code = code.replace('t.type', 't["type"]')
code = code.replace('t.value', 't["value"]')

# Restore true/false if needed? I'll leave 1 == 1 for now just to make sure.

with open('src/self_hosted/lexer.aayu', 'w') as f:
    f.write(code)
