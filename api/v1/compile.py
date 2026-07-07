from fastapi import APIRouter
from .models import CompileRequest
import sys
import os

# Append the prototype directory to path so we can import the language modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import Compiler
from compiler.frontend.vm import VM

router = APIRouter()

@router.post("/compile")
def compile_code(request: CompileRequest):
    try:
        # Lexing
        lexer = Lexer(request.code)
        tokens = lexer.tokenize()
        
        # We need a serializable version of tokens
        serializable_tokens = [{"type": t.type.name, "value": t.value, "line": t.line} for t in tokens]
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        # For AST serialization, we do a basic string representation for now 
        # since actual AST nodes might not be directly serializable without a schema.
        ast_repr = ast.stringify() if hasattr(ast, 'stringify') else str(ast)
        
        # Compiling
        compiler = Compiler()
        compiler.compile(ast)
        bytecode = compiler.bytecode
        
        # Bytecode serialization
        serializable_bytecode = [
            {"opcode": instr.opcode.name, "operands": instr.operands} 
            for instr in bytecode
        ]
        
        # Execution (VM)
        vm = VM()
        
        # Capture stdout
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            vm.execute(bytecode)
        
        output = f.getvalue()
        
        return {
            "success": True,
            "tokens": serializable_tokens,
            "ast": ast_repr,
            "bytecode": serializable_bytecode,
            "output": output
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
