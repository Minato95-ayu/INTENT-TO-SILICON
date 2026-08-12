import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser

def to_dict(node):
    if isinstance(node, list):
        return [to_dict(n) for n in node]
    if hasattr(node, "__dict__"):
        d = {}
        for k, v in node.__dict__.items():
            if k not in ['line', 'column']:
                d[k] = to_dict(v)
        return d
    return node

def test_differential():
    source = '''
    app "MyApp"
    
    fn main() {
        let x = 10.
        let y = x + 5.
    }
    
    model User {
        id: Int
        name: String
    }
    '''
    
    tokens1 = Lexer(source).tokenize()
    ast1 = Parser(tokens1).parse()
    
    dict1 = to_dict(ast1)
    serialized1 = json.dumps(dict1, sort_keys=True)
    
    tokens2 = Lexer(source).tokenize()
    ast2 = Parser(tokens2).parse()
    
    dict2 = to_dict(ast2)
    serialized2 = json.dumps(dict2, sort_keys=True)
    
    if serialized1 == serialized2:
        print("Differential Parsing Passed: Both ASTs match exactly.")
        return True
    else:
        print("Differential Parsing Failed: AST mismatch!")
        return False

if __name__ == "__main__":
    success = test_differential()
    sys.exit(0 if success else 1)
