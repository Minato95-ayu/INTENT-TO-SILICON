# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# ==============================================================================

from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.middleware.cors import CORSMiddleware
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
import traceback
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://intent-to-silicon.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompileRequest(BaseModel):
    code: str

@app.post("/api/v1/compile")
def compile_code(req: CompileRequest):
    errors = []
    tokens_out = []
    ast_out = None
    bytecode_out = []
    vm_output = ""
    
    # Capture prints
    old_stdout = sys.stdout
    stdout_buffer = io.StringIO()
    sys.stdout = stdout_buffer
    
    try:
        lexer = Lexer(req.code)
        tokens = lexer.tokenize()
        tokens_out = [str(t) for t in tokens]
        
        parser = Parser(tokens)
        ast = parser.parse()
        ast_out = {"type": "Program"} # Keeping it simple for JSON serialization
        
        analyzer = SemanticAnalyzer()
        ast = analyzer.analyze(ast)
        
        pipeline = IRPipeline()
        hir = pipeline.to_hir(ast)
        mir = pipeline.to_mir(hir)
        lir = pipeline.to_lir(mir)
        
        prog = BytecodeEncoder().encode(lir)
        
        import compiler.bytecode.instructions as instr
        idx = 0
        while idx < len(prog.bytecode) - 2:
            op = prog.bytecode[idx]
            if op == instr.Opcode.HALT:
                bytecode_out.append("HALT")
                break
            try:
                op_name = next(k for k, v in instr.Opcode.__dict__.items() if v == op and not k.startswith('_'))
            except StopIteration:
                op_name = str(op)
            arg = (prog.bytecode[idx+1] << 8) | prog.bytecode[idx+2]
            bytecode_out.append(f"{op_name} {arg}")
            idx += 3
            
        # Run VM
        from runtime.session.manager import SessionManager
        import uuid
        manager = SessionManager(prog)
        session = manager.get_or_create_session(str(uuid.uuid4()))
        if "__PAGE_START__" in session.vm.action_addresses:
            session.vm.call_action_by_name("__PAGE_START__")
            vm_output += "PAGE RENDERED. "
        elif "main" in session.vm.action_addresses:
            session.vm.call_action_by_name("main")
            
        sys.stdout = old_stdout
        vm_output += stdout_buffer.getvalue()
            
    except Exception as e:
        sys.stdout = old_stdout
        errors.append(f"{type(e).__name__}: {str(e)}")
        # traceback.print_exc()

    return {
        "success": len(errors) == 0,
        "tokens": tokens_out,
        "ast": ast_out,
        "bytecode": bytecode_out,
        "vm_output": vm_output.strip(),
        "errors": errors
    }

@app.get("/health")
def health():
    return {"status": "ok", "version": "v1.1"}
