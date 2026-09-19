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

with open('compiler/lexer/lexer.py', 'r') as f:
    content = f.read()

# Replace Token(...) calls with Token(..., self._get_source_line(self.line))
# But need to be careful with Token() in methods.
content = re.sub(r'Token\((TokenType\.\w+), (.*?), (self\.line), (.*?)\)', r'Token(\1, \2, \3, \4, self._get_source_line(\3))', content)

with open('compiler/lexer/lexer.py', 'w') as f:
    f.write(content)
print("Updated lexer.py")
