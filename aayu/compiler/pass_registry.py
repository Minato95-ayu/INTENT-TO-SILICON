from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Type
from aayu.compiler.errors import DiagnosticEngine

@dataclass
class PassMetadata:
    name: str
    description: str
    is_analysis: bool = False
    
@dataclass
class PassDefinition:
    meta: PassMetadata
    dependencies: List[str] = field(default_factory=list)
    invalidates: List[str] = field(default_factory=list)
    execute: Callable[[Any, DiagnosticEngine], Any] = None

class PassRegistry:
    """
    Centralized registry for all compiler passes.
    Tracks dependencies and cache invalidation rules.
    """
    _passes: Dict[str, PassDefinition] = {}

    @classmethod
    def register(cls, meta: PassMetadata, dependencies: List[str] = None, invalidates: List[str] = None):
        def decorator(func):
            deps = dependencies or []
            invals = invalidates or []
            if meta.is_analysis:
                # Analysis passes typically don't invalidate anything
                invals = []
            
            definition = PassDefinition(
                meta=meta,
                dependencies=deps,
                invalidates=invals,
                execute=func
            )
            cls._passes[meta.name] = definition
            return func
        return decorator

    @classmethod
    def get_pass(cls, name: str) -> PassDefinition:
        if name not in cls._passes:
            raise ValueError(f"Compiler pass '{name}' not found in registry.")
        return cls._passes[name]

    @classmethod
    def list_passes(cls) -> List[PassMetadata]:
        return [p.meta for p in cls._passes.values()]

class PassManager:
    """
    Executes a series of passes from the PassRegistry.
    Handles dependency resolution, validation, and invalidation.
    """
    def __init__(self, diag: DiagnosticEngine):
        self.diag = diag
        self.valid_analyses = set()
    
    def run_pipeline(self, pipeline: List[str], state: Any) -> Any:
        for pass_name in pipeline:
            state = self.run_pass(pass_name, state)
        return state

    def run_pass(self, pass_name: str, state: Any) -> Any:
        pdef = PassRegistry.get_pass(pass_name)
        
        # Ensure dependencies are met
        for dep in pdef.dependencies:
            if dep not in self.valid_analyses:
                # Automatically run required analysis if missing
                state = self.run_pass(dep, state)
                
        # Execute
        result = pdef.execute(state, self.diag)
        
        if pdef.meta.is_analysis:
            self.valid_analyses.add(pass_name)
        else:
            # Invalidate cached analyses
            for inv in pdef.invalidates:
                if inv == "*":
                    self.valid_analyses.clear()
                elif inv in self.valid_analyses:
                    self.valid_analyses.remove(inv)
                    
        # Future: Run Continuous IR Validators here
        
        return result
