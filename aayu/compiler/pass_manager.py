from abc import ABC, abstractmethod
from typing import Any, List, Type

class CompilerPass(ABC):
    @abstractmethod
    def run(self, node: Any) -> Any:
        pass
        
    def verify(self, node: Any) -> bool:
        return True
        
    def invalidate(self) -> None:
        pass

class AnalysisPass(CompilerPass):
    """Passes that do not mutate the AST/IR but gather information."""
    pass

class OptimizationPass(CompilerPass):
    """Passes that mutate the AST/IR to improve performance."""
    pass

class VerificationPass(CompilerPass):
    """Passes that verify the correctness of the IR."""
    pass

class LoweringPass(CompilerPass):
    """Passes that lower IR from one level to another (e.g. HIR -> MIR)."""
    pass

class AnalysisManager:
    """Manages cached analyses and invalidation for passes."""
    def __init__(self):
        self.cache: dict[Type[AnalysisPass], AnalysisPass] = {}
        
    def get_analysis(self, pass_type: Type[AnalysisPass], func: Any) -> AnalysisPass:
        if pass_type not in self.cache:
            p = pass_type()
            p.run(func)
            self.cache[pass_type] = p
        return self.cache[pass_type]
        
    def invalidate(self, pass_type: Type[AnalysisPass]):
        if pass_type in self.cache:
            del self.cache[pass_type]
            
    def invalidate_all(self):
        self.cache.clear()

class PassManager:
    """
    AAYU Generic Compiler Pass Manager
    Orchestrates the execution of different passes using a dependency graph.
    """
    def __init__(self):
        self.passes: dict[Type[CompilerPass], CompilerPass] = {}
        self.analysis_manager = AnalysisManager()

    def register_pass(self, p: CompilerPass):
        self.passes[type(p)] = p

    def run(self, module: Any, context: Any = None) -> Any:
        # Topological sort based on requires
        order = self._resolve_dependencies()
        
        current_node = module
        for pass_type in order:
            p = self.passes[pass_type]
            if hasattr(p, 'analysis_manager'):
                p.analysis_manager = self.analysis_manager
            
            # Pass execution returns the mutated state or just diagnostics/metadata depending on the pass type
            if context:
                if hasattr(p, "run_with_context"):
                    current_node = p.run_with_context(current_node, context)
                else:
                    current_node = p.run(current_node)
            else:
                current_node = p.run(current_node)
                
            if not p.verify(current_node):
                raise Exception(f"Pass {pass_type.__name__} failed verification!")
        return current_node
        
    def _resolve_dependencies(self) -> List[Type[CompilerPass]]:
        visited = set()
        temp_mark = set()
        order = []
        
        def visit(ptype: Type[CompilerPass]):
            if ptype in temp_mark:
                raise Exception(f"Circular dependency detected involving pass {ptype.__name__}")
            if ptype not in visited:
                temp_mark.add(ptype)
                p = self.passes.get(ptype)
                if not p:
                    raise Exception(f"Required pass {ptype.__name__} is not registered.")
                
                # Visit requirements
                requires = getattr(ptype, 'requires', [])
                for req in requires:
                    visit(req)
                    
                temp_mark.remove(ptype)
                visited.add(ptype)
                order.append(ptype)
                
        for ptype in self.passes.keys():
            if ptype not in visited:
                visit(ptype)
                
        return order

    def invalidate_all(self):
        self.analysis_manager.invalidate_all()
        for p in self.passes.values():
            p.invalidate()
