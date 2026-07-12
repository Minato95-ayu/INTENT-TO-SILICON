import os

api_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\api'
os.makedirs(api_dir, exist_ok=True)

api_main_content = """\
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Add prototype root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from language.lexer import Lexer
from language.parser import Parser
from language.compiler import Compiler
from language.runtime.vm import VirtualMachine

app = FastAPI(title="AAYU Compiler API")

class CompileRequest(BaseModel):
    code: str

@app.post("/api/compile")
def compile_code(req: CompileRequest):
    try:
        # AAYU Execution Pipeline
        lexer = Lexer(req.code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        compiler = Compiler()
        bytecode = compiler.compile(ast)
        
        # Capture stdout
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            vm = VirtualMachine()
            vm.run(bytecode)
        
        output = f.getvalue()
        
        return {
            "status": "success",
            "ast": ast,
            "bytecode": bytecode,
            "output": output
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
"""

with open(os.path.join(api_dir, 'main.py'), 'w', encoding='utf-8') as f:
    f.write(api_main_content)

print("Created api/main.py")
