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

import argparse
import sys
import os
import subprocess

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.ast.nodes import *

def handle(args):
    parser = argparse.ArgumentParser(description="Compile AAYU to Native Executable via C Backend")
    parser.add_argument("file", help="AAYU file to compile")
    parser.add_argument("-o", "--output", help="Output executable name")
    
    # We parse manually since args is just a list passed from cli.py
    parsed_args, unknown = parser.parse_known_args(args)
    
    file_path = parsed_args.file
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
        
    out_name = parsed_args.output
    if not out_name:
        out_name = os.path.splitext(os.path.basename(file_path))[0]
        if os.name == 'nt':
            out_name += ".exe"
            
    c_out = f"{out_name.replace('.exe', '')}.c"
    
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()
        
    print(f"[AAYU Native Builder] Parsing {file_path}...")
    lexer = Lexer(src)
    tokens = lexer.tokenize()
    parser_obj = Parser(tokens)
    ast = parser_obj.parse()
    
    print("[AAYU Native Builder] Transpiling AST to C Code...")
    c_code = compile_to_c(ast)
    
    with open(c_out, "w", encoding="utf-8") as f:
        f.write(c_code)
        
    print(f"[AAYU Native Builder] Invoking GCC Compiler on {c_out}...")
    try:
        subprocess.run(["gcc", c_out, "-o", out_name], check=True)
        print(f"[AAYU Native Builder] Success! Created ultra-fast native executable: {out_name}")
    except subprocess.CalledProcessError as e:
        print(f"[AAYU Native Builder] Compilation failed with error code {e.returncode}")
    except FileNotFoundError:
        print("[AAYU Native Builder] Error: 'gcc' not found. Ensure GCC/MinGW is installed and in PATH.")


def compile_to_c(ast):
    output = []
    def emit(s):
        output.append(s)
        
    emit("#include <stdio.h>\n")
    emit("#include <stdlib.h>\n")
    emit("#include <string.h>\n\n")
    emit("int main() {\n")
    
    def compile_expr(node):
        if isinstance(node, LiteralNode):
            return str(node.value)
            
        if isinstance(node, IdentifierNode):
            return node.name
            
        if isinstance(node, BinaryOpNode):
            left = compile_expr(node.left)
            right = compile_expr(node.right)
            return f"({left} {node.operator} {right})"
            
        if isinstance(node, ActionCallNode):
            if node.name == "print":
                arg = compile_expr(node.args[0])
                return f'printf("%f\\n", (double){arg})'
                
        return "0"

    def compile_stmt(stmt, indent):
        ind = "    " * indent
        
        if isinstance(stmt, LetDeclarationNode):
            val = compile_expr(stmt.value)
            emit(f"{ind}double {stmt.name} = {val};\n")
            
        elif isinstance(stmt, AssignmentNode):
            target = getattr(stmt.target, "name", stmt.target) if hasattr(stmt.target, "name") else stmt.target
            val = compile_expr(stmt.value)
            emit(f"{ind}{target} = {val};\n")
            
        elif isinstance(stmt, WhileNode):
            cond = compile_expr(stmt.condition)
            emit(f"{ind}while ({cond}) {{\n")
            for b in stmt.body:
                compile_stmt(b, indent + 1)
            emit(f"{ind}}}\n")
            
        elif isinstance(stmt, ActionCallNode):
            if stmt.name == "print":
                arg = compile_expr(stmt.args[0])
                emit(f'{ind}printf("%f\\n", (double){arg});\n')
            
    if isinstance(ast, ProgramNode):
        for stmt in ast.statements:
            compile_stmt(stmt, 1)
            
    emit("    return 0;\n")
    emit("}\n")
    
    return "".join(output)
