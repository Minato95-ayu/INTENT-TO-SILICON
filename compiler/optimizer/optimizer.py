from typing import List
from compiler.ir.lir import LIRNode
from .passes import OptimizationPass

class Optimizer:
    def __init__(self):
        self.passes: List[OptimizationPass] = []
        
    def register_pass(self, opt_pass: OptimizationPass):
        self.passes.append(opt_pass)
        
    def optimize(self, lir: List[LIRNode]) -> List[LIRNode]:
        current_lir = lir
        for opt_pass in self.passes:
            current_lir = opt_pass.run(current_lir)
        return current_lir
