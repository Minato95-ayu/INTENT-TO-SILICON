
import sys
import os

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.ast.nodes import ImportNode

def parse_file(path):
    print(f"Parsing {path}...")
    with open(path, "r", encoding="utf-8") as mf:
        mod_source = mf.read()
    return Parser(Lexer(mod_source).tokenize()).parse()

print("Starting...")
target = "stthomas_app/app.aayu"
ast = parse_file(target)
print("Main AST parsed!")

def load_imports(program_node, base_dir, visited):
    new_statements = []
    for stmt in program_node.statements:
        if isinstance(stmt, ImportNode):
            mod_path = stmt.module.replace(".", "/") + ".aayu"
            full_path = os.path.join(base_dir, mod_path)
            
            print(f"Checking import: {full_path}")
            if full_path not in visited:
                visited.add(full_path)
                if os.path.exists(full_path):
                    mod_ast = parse_file(full_path)
                    print(f"Recursively loading imports for {full_path}")
                    mod_ast = load_imports(mod_ast, base_dir, visited)
                    print(f"Extending statements for {full_path}")
                    new_statements.extend(mod_ast.statements)
                else:
                    print(f"Error: Module {stmt.module} not found at {full_path}")
        else:
            new_statements.append(stmt)
    return program_node

base_directory = os.path.dirname(os.path.abspath(target))
print("Loading imports...")
final_ast = load_imports(ast, base_directory, set([os.path.abspath(target)]))
print("Done!")

