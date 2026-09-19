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

class OptimizationPass:
    def run(self, lir: List[LIRNode]) -> List[LIRNode]:
        raise NotImplementedError()

class DeadCodeElimination(OptimizationPass):
    def run(self, lir: List[LIRNode]) -> List[LIRNode]:
        # Very simple DCE: if a state is INIT'd but never GET'd or SET'd, remove the INIT.
        used_states = set()
        for node in lir:
            if node.opcode in ["STATE_GET", "STATE_SET"]:
                used_states.add(node.operands[0])
                
        optimized = []
        for node in lir:
            if node.opcode == "STATE_INIT":
                if node.operands[0] not in used_states:
                    continue # Skip this initialization, it's dead code
            optimized.append(node)
            
        return optimized
