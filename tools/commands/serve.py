import sys
import os
import time
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.renderers.web_renderer import WebRenderer
from runtime.session.manager import SessionManager

def resolve_imports(source: str, base_dir: str, loaded=None) -> str:
    if loaded is None:
        loaded = set()
    lines = source.split('\n')
    out = []
    for line in lines:
        sline = line.strip()
        if sline.startswith("import "):
            module_name = sline.split(" ")[1].strip()
            if module_name in loaded:
                continue
            loaded.add(module_name)
            module_path = os.path.join(base_dir, module_name.replace(".", os.sep) + ".aayu")
            if os.path.exists(module_path):
                with open(module_path, "r", encoding="utf-8") as f:
                    mod_src = f.read()
                    out.append(resolve_imports(mod_src, base_dir, loaded))
            else:
                print(f"[Warning] Could not find imported module: {module_path}")
        else:
            out.append(line)
    return "\n".join(out)

def handle(args):
    if len(args) < 1:
        print("Usage: aayu serve <file.aayu>")
        sys.exit(1)
        
    source_file = args[0]
    if not os.path.exists(source_file):
        print(f"Error: Target file {source_file} not found.")
        sys.exit(1)
        
    source = open(source_file, encoding="utf-8").read()
    
    # Pre-process imports
    source = resolve_imports(source, os.path.dirname(os.path.abspath(source_file)) or ".")
    
    print(f"[AAYU] Serving {source_file} on web renderer...")
    
    # 1. Compilation
    l = Lexer(source)
    ast = Parser(l.tokenize()).parse()
    ast = SemanticAnalyzer().analyze(ast)
    pipe = IRPipeline()
    hir = pipe.to_hir(ast)
    mir = pipe.to_mir(hir)
    lir = pipe.to_lir(mir)
    prog = BytecodeEncoder().encode(lir)

    # 2. Session Manager Initialization
    session_manager = SessionManager(prog)

    # 3. Web Renderer Initialization
    port = int(os.environ.get("PORT", 3000))
    renderer = WebRenderer(session_manager, project_dir=".", port=port)
    renderer.initialize()

    # 4. Render Loop (Cleanup Thread)
    try:
        while True:
            session_manager.cleanup_stale_sessions()
            time.sleep(10)
    except KeyboardInterrupt:
        renderer.shutdown()
        print("Shutting down...")
