import os
import pytest
import json
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.bytecode.encoder import BytecodeEncoder

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "examples")
SNAPSHOTS_DIR = os.path.join(os.path.dirname(__file__), "snapshots")

if not os.path.exists(SNAPSHOTS_DIR):
    os.makedirs(SNAPSHOTS_DIR)

EXAMPLES = ["hello.aayu", "calculator.aayu", "crud.aayu", "crm.aayu"]

def serialize_ast(node):
    if hasattr(node, "__dict__"):
        result = {}
        for k, v in node.__dict__.items():
            if k in ["line", "column"]: # Skip exact lines as they might fluctuate
                continue
            if isinstance(v, list):
                result[k] = [serialize_ast(item) for item in v]
            elif isinstance(v, dict):
                result[k] = {key: serialize_ast(val) for key, val in v.items()}
            else:
                result[k] = serialize_ast(v)
        # Add node type
        result["__type__"] = node.__class__.__name__
        return result
    return node

@pytest.mark.parametrize("filename", EXAMPLES)
def test_golden_ast_and_bytecode(filename):
    filepath = os.path.join(EXAMPLES_DIR, filename)
    with open(filepath, "r") as f:
        source = f.read()

    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    compiler = BytecodeEncoder()
    bytecode = compiler.compile(ast)
    
    ast_snapshot_path = os.path.join(SNAPSHOTS_DIR, f"{filename}.ast.json")
    bytecode_snapshot_path = os.path.join(SNAPSHOTS_DIR, f"{filename}.bc.txt")
    
    ast_json = json.dumps(serialize_ast(ast), indent=2)
    bytecode_txt = str(bytecode)
    
    if os.environ.get("UPDATE_SNAPSHOTS") == "1" or not os.path.exists(ast_snapshot_path):
        with open(ast_snapshot_path, "w") as f:
            f.write(ast_json)
        with open(bytecode_snapshot_path, "w") as f:
            f.write(bytecode_txt)
        pytest.skip(f"Snapshot updated/created for {filename}")
        
    with open(ast_snapshot_path, "r") as f:
        expected_ast_json = f.read()
        
    with open(bytecode_snapshot_path, "r") as f:
        expected_bytecode_txt = f.read()
        
    assert ast_json == expected_ast_json, f"AST snapshot mismatch for {filename}"
    assert bytecode_txt == expected_bytecode_txt, f"Bytecode snapshot mismatch for {filename}"
