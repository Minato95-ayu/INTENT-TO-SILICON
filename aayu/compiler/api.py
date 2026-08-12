from typing import Optional, List, Any
import time

from aayu.compiler.errors import DiagnosticEngine, DiagnosticSeverity, CompilerError
from aayu.compiler.metrics import CompilerMetrics
from aayu.compiler.validators import (
    validate_ast, validate_hir, validate_mir, 
    validate_ssa, validate_lir, validate_bytecode
)

# Placeholders for actual internal modules
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
# Semantic, HIR, MIR imports to be wired...
# from aayu.compiler.backend.bytecode.emitter import BytecodeEmitter

class Compiler:
    """
    Public Compiler API for AAYU.
    Provides fine-grained lifecycle methods for language servers, 
    testing, and general compilation tasks.
    """
    def __init__(self):
        self.diag = DiagnosticEngine()
        self.metrics = CompilerMetrics()
        
        # State
        self.ast = None
        self.hir = None
        self.mir_cfgs = None
        self.ssa_cfgs = None
        self.lir_functions = None
        self.bytecode: Optional[bytes] = None

    def parse(self, source: str) -> bool:
        """Lexes and parses the source into an AST."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, diag=self.diag)
        
        try:
            self.ast = parser.parse()
            if not validate_ast(self.ast, self.diag):
                return False
        except Exception as e:
            self.diag.report(DiagnosticSeverity.ERROR, f"Parse error: {e}")
            return False
            
        self.metrics.ast_nodes = 1 # TODO: Count actual nodes
        return True

    def semantic(self) -> bool:
        """Performs semantic analysis (scope, symbols, types)."""
        if not self.ast:
            return False
        # TODO: Run semantic pipeline
        return True

    def hir(self) -> bool:
        """Lowers AST to High-Level IR."""
        if not self.ast:
            return False
        # TODO: Lower to HIR
        # validate_hir(self.hir, self.diag)
        return True

    def mir(self) -> bool:
        """Lowers HIR to Register-based MIR (CFG)."""
        if not self.hir:
            return False
        # TODO: Lower to MIR
        # validate_mir(self.mir_cfgs, self.diag)
        return True

    def ssa(self) -> bool:
        """Converts MIR to SSA form."""
        if not self.mir_cfgs:
            return False
        # TODO: SSA Construction
        # validate_ssa(self.ssa_cfgs, self.diag)
        return True

    def optimize(self) -> bool:
        """Runs the optimization pipeline on SSA."""
        self.metrics.start_timer()
        # TODO: Run Optimizer (Constant folding, DCE, etc.)
        self.metrics.optimization_time_ms = self.metrics.stop_timer()
        return True

    def allocate(self) -> bool:
        """Performs Register Allocation (Linear Scan & Spilling)."""
        self.metrics.start_timer()
        # TODO: Run Register Allocator
        self.metrics.allocation_time_ms = self.metrics.stop_timer()
        return True

    def lir(self) -> bool:
        """Generates Linear IR (removes PHIs, finalizes virtual registers)."""
        if not self.ssa_cfgs: # Technically uses allocated SSA
            return False
        # TODO: LIR Generation
        # validate_lir(self.lir_functions, self.diag)
        return True

    def generate_bytecode(self) -> bool:
        """Emits AYBC custom binary format."""
        # TODO: Emit bytecode using BytecodeEmitter
        # validate_bytecode(self.bytecode, self.diag)
        return True

    # --- Lifecycle Methods ---

    def compile_text(self, source: str) -> bool:
        self.metrics.start_timer()
        
        try:
            if not self.parse(source): return False
            if not self.semantic(): return False
            if not self.hir(): return False
            if not self.mir(): return False
            if not self.ssa(): return False
            if not self.optimize(): return False
            if not self.allocate(): return False
            if not self.lir(): return False
            if not self.generate_bytecode(): return False
            
        except CompilerError:
            pass
            
        self.metrics.compile_time_ms = self.metrics.stop_timer()
        return not self.diag.has_errors()

    def compile_file(self, filepath: str) -> bool:
        with open(filepath, 'r') as f:
            return self.compile_text(f.read())
            
    def compile_workspace(self, root_dir: str) -> bool:
        """
        Phase 2 Multi-file Frontend Entrypoint.
        Orchestrates Workspace -> DAG -> Planner -> Parsers -> Semantic.
        """
        from aayu.compiler.workspace import WorkspaceLoader
        from aayu.compiler.graph import ModuleGraph
        from aayu.compiler.cache import IncrementalCache, BuildPlanner
        from aayu.compiler.ast.nodes import ProjectNode
        
        self.metrics.start_timer()
        
        # 1. Architecture Pipeline
        loader = WorkspaceLoader(root_dir)
        loader.load()
        graph = ModuleGraph(loader)
        graph.build_graph()
        
        cache = IncrementalCache(root_dir)
        planner = BuildPlanner(graph, cache)
        
        try:
            order, actions = planner.plan()
        except Exception as e:
            self.diag.report(DiagnosticSeverity.ERROR, str(e))
            return False
            
        # 2. Multi-file Parser & Cache
        project_modules = {}
        for node in order:
            action = actions[node.id]
            if action == "Skip":
                ast = cache.load_ast(node.id)
                if ast is None:
                    action = "Compile" # Fallback if cache file missing
                else:
                    project_modules[node.id] = ast
                    continue
                    
            if action == "Compile":
                with open(node.path, "r") as f:
                    source = f.read()
                
                lexer = Lexer(source)
                parser = Parser(lexer.tokenize(), diag=self.diag)
                
                try:
                    prog_ast = parser.parse()
                    if not validate_ast(prog_ast, self.diag):
                        return False
                    
                    project_modules[node.id] = prog_ast
                    
                    # Update node state and save cache
                    node.ast_hash = "TODO_AST_HASH"
                    node.compile_state = "Parsed"
                    cache.save_ast(node.id, prog_ast)
                    cache.update_module_cache(node)
                except Exception as e:
                    self.diag.report(DiagnosticSeverity.ERROR, f"Parse error in {node.id}: {e}")
                    return False
                    
        # Construct the frozen ProjectNode
        self.ast = ProjectNode(line=0, column=0, modules=project_modules)
        
        # 3. Initialize Semantic Context
        from aayu.compiler.semantic.context import SemanticContext
        ctx = SemanticContext(self.diag)
        
        # Reset Node Counter for deterministic reproducible builds
        from aayu.compiler.ast.nodes import reset_node_counter
        reset_node_counter()
        
        # 4. Execute Pass Manager
        from aayu.compiler.pass_manager import PassManager
        from aayu.compiler.semantic.scope_pass import ScopePass
        from aayu.compiler.semantic.symbol_pass import SymbolPass
        from aayu.compiler.semantic.type_pass import TypePass
        
        pm = PassManager()
        pm.register_pass(ScopePass())
        pm.register_pass(SymbolPass())
        pm.register_pass(TypePass())
        
        try:
            self.ast = pm.run(self.ast, ctx)
            self.project_scope = ctx.project_scope
        except Exception as e:
            self.diag.report(DiagnosticSeverity.ERROR, f"PassManager failed: {str(e)}")
        
        self.metrics.compile_time_ms = self.metrics.stop_timer()
        return not self.diag.has_errors()

    def run(self):
        """Executes the compiled bytecode inside the VM."""
        if not self.bytecode:
            raise RuntimeError("No bytecode available to run. Compile first.")
            
        from aayu.runtime.vm.vm import VirtualMachine
        vm = VirtualMachine()
        vm.load_aybc(self.bytecode)
        if "main" in vm.action_addresses:
            vm.call_action_by_name("main")

    def disassemble(self) -> str:
        """Returns the disassembled bytecode representation."""
        if not self.bytecode:
            return "No bytecode to disassemble."
        return "Disassembly not yet implemented."

    def dump(self, phase: str) -> str:
        """Dumps internal representations (ast, hir, mir, ssa, lir)."""
        return f"Dump of {phase}"

    def benchmark(self) -> CompilerMetrics:
        """Returns collected compilation metrics."""
        return self.metrics
