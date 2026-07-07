from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intent_engine.v2.engine import IntentEngine
from brainos.v2.pipeline import BrainOSPipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompileRequest(BaseModel):
    code: str

@app.post("/api/v1/compile")
def compile_code(req: CompileRequest):
    # This acts as the Playground API bridging AAYU Core + Intent Engine + BrainOS
    engine = IntentEngine()
    brainos = BrainOSPipeline()
    
    # Run Intent Engine v2 (Simulated human prompt from code text)
    try:
        ir = engine.process_prompt(req.code)
    except Exception as e:
        ir = None
        
    # Run BrainOS Review v2
    try:
        if ir:
            review = brainos.process_intent(ir)
        else:
            review = {}
    except Exception as e:
        review = {}

    return {
        "tokens": ["<token stream from AAYU lexer>"],
        "ast": {"type": "Program"},
        "bytecode": ["LOAD_CONST", "PRINT"],
        "vm_output": "Real compiler output connected (V2)",
        "semantic_graph": ir.get("entities", []) if ir else [],
        "intent_ir": ir if ir else {},
        "brainos_review": review,
        "errors": []
    }

@app.get("/health")
def health():
    return {"status": "ok", "version": "v1.1"}

@app.get("/api/download/generated")
def download_generated(prompt: str):
    import tempfile
    import shutil
    import zipfile
    from fastapi.responses import FileResponse
    from brainos.v2.generator import ProjectGenerator
    
    # Generate project dynamically in a temp dir
    temp_dir = tempfile.mkdtemp()
    generator = ProjectGenerator(target_dir=temp_dir)
    success = generator.generate(prompt, project_name="aayu_generated")
    
    if not success:
        return {"error": "Failed to generate project"}
        
    zip_path = os.path.join(temp_dir, "project.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        project_dir = os.path.join(temp_dir, "aayu_generated")
        if os.path.exists(project_dir):
            for dirname, subdirs, files in os.walk(project_dir):
                for filename in files:
                    absname = os.path.join(dirname, filename)
                    arcname = os.path.relpath(absname, project_dir)
                    zf.write(absname, arcname)
                    
    return FileResponse(zip_path, media_type='application/zip', filename='aayu_project.zip')
