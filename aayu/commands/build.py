import sys
import os

def handle(args):
    target = None
    if len(args) > 0 and not args[0].startswith("-"):
        target = args[0]
        
    if not target:
        from aayu.package.manifest import AayuManifest
        manifest = AayuManifest()
        if manifest.exists():
            target = manifest.get_entry()
        else:
            target = "src/main.aayu"

    output_path = "dist/app.ayc"
    
    for i, arg in enumerate(args):
        if arg == "-o" or arg == "--output":
            if i + 1 < len(args):
                output_path = args[i+1]
                
    if not os.path.exists(target):
        print(f"Error: Target '{target}' not found.")
        sys.exit(1)
        
    print(f"[AAYU] Building {target} to bytecode...")
        
    try:
        from aayu.compiler.lexer.lexer import Lexer
        from aayu.compiler.parser.parser import Parser
        from aayu.compiler.semantic.analyzer import SemanticAnalyzer
        from aayu.compiler.ir.pipeline import IRPipeline
        from aayu.compiler.bytecode.encoder import BytecodeEncoder
        from aayu.compiler.ast.nodes import ImportNode, ProgramNode
        
        with open(target, "r", encoding="utf-8") as f:
            source = f.read()
            
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        from aayu.compiler.ast_resolver import resolve_ast_imports
        base_directory = os.path.dirname(os.path.abspath(target))
        if not base_directory:
            base_directory = "."
            
        ast = resolve_ast_imports(ast, base_directory, set([os.path.abspath(target)]))
        
        semantic_ast = SemanticAnalyzer().analyze(ast)
        
        from aayu.compiler.semantic.type_inference import TypeInference
        semantic_ast = TypeInference().infer(semantic_ast)
        
        from aayu.compiler.semantic.type_checker import TypeChecker
        TypeChecker().check(semantic_ast)
        
        ir_pipeline = IRPipeline()
        lir = ir_pipeline.to_lir(ir_pipeline.to_mir(ir_pipeline.to_hir(semantic_ast)))
        
        program = BytecodeEncoder().encode(lir)
        
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(program.serialize_to_binary())
            
        print(f"[AAYU] Successfully built {target} to {output_path}")
        
    except Exception as e:
        print(f"\nBuild Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
