import sys
import time

from aayu.compiler.ast.nodes import (
    ProgramNode, ActionDeclarationNode,
    AssignmentNode, LiteralNode, IdentifierNode
)
from aayu.compiler.semantic.pipeline import SemanticPipeline

def generate_massive_ast(size=10000):
    statements = []
    for i in range(size):
        assign = AssignmentNode(
            line=i+1, column=0,
            target=IdentifierNode(line=i+1, column=0, name=f"x{i}"),
            value=LiteralNode(line=i+1, column=5, value=i)
        )
        statements.append(assign)
    
    action = ActionDeclarationNode(
        line=1, column=0,
        name="stress_test",
        statements=statements,
        args=[],
        return_type=None
    )
    
    return ProgramNode(line=1, column=0, statements=[action])

if __name__ == "__main__":
    print("Generating AST with 10,000 nodes...")
    ast = generate_massive_ast(10000)
    
    print("Running SemanticPipeline (Semantic + HIR-3 Validation)...")
    start_time = time.time()
    
    pipeline = SemanticPipeline()
    hir = pipeline.run(ast)
    
    duration = time.time() - start_time
    print(f"Time taken: {duration:.4f} seconds")
    
    if pipeline.diag_engine.has_errors():
        print("Stress test failed with diagnostic errors:")
        pipeline.diag_engine.print_all()
        sys.exit(1)
        
    if not hir:
        print("Stress test failed to generate HIR.")
        sys.exit(1)
        
    print(f"Stress test PASSED. Generated HIR with {len(hir.actions[0].body.statements)} statements.")
    sys.exit(0)
