from typing import List
from compiler_context import CompilerContext
from .base import BasePass

class PassManager:
    def __init__(self):
        self.passes: List[BasePass] = []
        
    def add_pass(self, p: BasePass):
        self.passes.append(p)
        
    def run(self, context: CompilerContext) -> bool:
        for p in self.passes:
            success = p.run(context)
            if context.diagnostics.has_errors() or not success:
                context.diagnostics.error(f"Compilation stopped due to errors in pass: {p.name}", context.current_module)
                return False
        return True
