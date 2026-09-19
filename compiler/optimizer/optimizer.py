# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

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
