import sys
sys.path.insert(0, ".")
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
with open("demo_app.aayu") as f:
    code = f.read()
lexer = Lexer(code)
parser = Parser(lexer.tokenize())
ast = parser.parse()

def dump(node, indent=0):
    if not node: return
    ind = "  " * indent
    name = node.__class__.__name__
    print(f"{ind}{name}: {getattr(node, 'widget_type', getattr(node, 'name', ''))}")
    if hasattr(node, "props"):
        for k, v in getattr(node, "props", {}).items():
            print(f"{ind}  prop {k} = {v.__class__.__name__}")
    if hasattr(node, "children"):
        for c in node.children:
            dump(c, indent+1)
    if hasattr(node, "body"):
        for c in node.body:
            dump(c, indent+1)
    if hasattr(node, "methods"):
        for m in node.methods:
            dump(m, indent+1)
    if hasattr(node, "statements"):
        for d in node.statements:
            dump(d, indent+1)

dump(ast)
