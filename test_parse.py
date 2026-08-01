from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
code = """action login(email, password)
    if email == "bench@test.com"
        if password == "password"
            return "mock_token_12345"
        end
    end
end"""
lexer = Lexer(code)
parser = Parser(lexer.tokenize())
ast = parser.parse()

def to_dict(node):
    if isinstance(node, list):
        return [to_dict(n) for n in node]
    if not hasattr(node, '__dict__'):
        return node
    d = {'__class__': node.__class__.__name__}
    for k, v in node.__dict__.items():
        d[k] = to_dict(v)
    return d

import json
print(json.dumps(to_dict(ast), indent=2))
