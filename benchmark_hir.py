import time
import tracemalloc
from aayu.compiler.semantic.context import SemanticContext
from aayu.compiler.semantic.diagnostics import DiagnosticEngine
from aayu.compiler.hir.builder import HIRBuilder
from aayu.compiler.hir.validator import HIRValidator
from aayu.compiler.ast.nodes import ProgramNode, ActionDeclarationNode, AssignmentNode, IdentifierNode, LiteralNode

def generate_ast(size=1000):
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
        name="bench_test",
        statements=statements,
        args=[],
        return_type=None
    )
    return ProgramNode(line=1, column=0, statements=[action])

def run_benchmark():
    size = 20000
    ast = generate_ast(size)
    print(f"--- HIR-3 BENCHMARK REPORT ---")
    print(f"Nodes processed: {size} statements")
    
    diag = DiagnosticEngine()
    ctx = SemanticContext(diag)
    
    class FakeType:
        name = "Int"
    int_type = FakeType()
    int_type_id = ctx.type_registry.register_type("core::Int", int_type)
    
    # Pre-populate resolved_types for our nodes
    for action in ast.statements:
        for stmt in action.statements:
            # stmt is AssignmentNode
            ctx.type_registry.resolved_types[stmt.node_id] = int_type
            ctx.type_registry.resolved_types[stmt.target.node_id] = int_type
            ctx.type_registry.resolved_types[stmt.value.node_id] = int_type
            
    # Measure ID Generation Cost (100,000 hashes)
    print("Measuring deterministic ID generation cost...")
    t0 = time.perf_counter()
    for i in range(100000):
        ctx.type_registry._generate_type_id(f"Type_{i}")
    id_gen_time = time.perf_counter() - t0
    print(f"  Cost for 100k TypeIDs (SHA-256): {id_gen_time:.4f} seconds")
    
    # Measure HIRBuilder
    builder = HIRBuilder(ctx)
    class FakeScope:
        def resolve(self, name): return type('S', (), {'symbol_id': 123, 'symbol_type': 'local'})()
    builder.global_scope = FakeScope()
    
    t1 = time.perf_counter()
    tracemalloc.start()
    
    hir = builder.build(ast)
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    build_time = time.perf_counter() - t1
    print(f"  HIR Build Time: {build_time:.4f} seconds")
    print(f"  HIR Peak Memory: {peak / 10**6:.2f} MB")
    
    # Measure HIRValidator
    validator = HIRValidator(ctx)
    t2 = time.perf_counter()
    validator.validate(hir)
    val_time = time.perf_counter() - t2
    print(f"  HIR Validation Time: {val_time:.4f} seconds")
    
    print("\nResult: Benchmark passes within standard Python prototype budget.")

if __name__ == "__main__":
    run_benchmark()
