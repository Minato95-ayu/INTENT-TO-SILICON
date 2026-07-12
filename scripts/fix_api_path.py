import os

api_path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\api\main.py'
with open(api_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("from language.lexer import Lexer", """
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from language.lexer import Lexer
""")

with open(api_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed sys.path")
