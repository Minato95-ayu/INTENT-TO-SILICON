import re

with open('compiler/lexer/lexer.py', 'r') as f:
    content = f.read()

# Replace Token(...) calls with Token(..., self._get_source_line(self.line))
# But need to be careful with Token() in methods.
content = re.sub(r'Token\((TokenType\.\w+), (.*?), (self\.line), (.*?)\)', r'Token(\1, \2, \3, \4, self._get_source_line(\3))', content)

with open('compiler/lexer/lexer.py', 'w') as f:
    f.write(content)
print("Updated lexer.py")
