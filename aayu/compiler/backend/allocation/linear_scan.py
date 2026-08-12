from typing import List, Dict
from collections import deque
from aayu.compiler.mir.nodes import FunctionMIR
from aayu.compiler.pass_manager import AnalysisPass
from aayu.compiler.backend.registers import LiveInterval, PhysicalRegister, RegisterClass

class LinearScanAllocationPass(AnalysisPass):
    """
    Implements Poletto and Sarkar's Linear Scan Register Allocation.
    Requires LiveIntervalConstructionPass to have run.
    """
    
    def __init__(self, num_registers: int = 4):
        self.num_registers = num_registers
        
        # Create physical registers (we'll just use GENERAL purpose ones for now)
        self.phys_regs = [
            PhysicalRegister(id=i, name=f"p{i}", kind=RegisterClass.GENERAL, width=64)
            for i in range(num_registers)
        ]
        
    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not func.blocks:
            return func
            
        if not hasattr(func, 'analysis') or 'intervals' not in func.analysis:
            raise Exception("Live Interval analysis required for Linear Scan Allocation.")
            
        intervals_dict: Dict[int, LiveInterval] = func.analysis['intervals']
        
        # Sort intervals by start point
        unhandled = sorted(intervals_dict.values(), key=lambda i: i.start)
        
        active: List[LiveInterval] = []
        free_regs = deque(self.phys_regs)
        
        next_spill_slot = 0
        
        for interval in unhandled:
            # 1. Expire old intervals
            # Find active intervals that end before or at the current interval's start
            expired = [a for a in active if a.end <= interval.start]
            for a in expired:
                active.remove(a)
                if a.assigned_register:
                    free_regs.append(a.assigned_register)
                    
            # 2. Check if we need to spill
            if not free_regs:
                # We must spill. We pick the interval with the lowest spill cost.
                # (Active intervals + current interval)
                candidates = active + [interval]
                # Tie-breaker: if costs are equal, spill the one that ends furthest in the future
                spill_cand = min(candidates, key=lambda i: (i.spill_cost, -i.end))
                
                if spill_cand == interval:
                    # Spill the current interval
                    interval.spill_slot = next_spill_slot
                    next_spill_slot += 1
                else:
                    # Spill an active interval, and steal its register for the current interval
                    interval.assigned_register = spill_cand.assigned_register
                    spill_cand.assigned_register = None
                    spill_cand.spill_slot = next_spill_slot
                    next_spill_slot += 1
                    
                    active.remove(spill_cand)
                    active.append(interval)
                    # Keep active sorted by end point
                    active.sort(key=lambda i: i.end)
            else:
                # We have a free register!
                interval.assigned_register = free_regs.popleft()
                active.append(interval)
                # Keep active sorted by end point
                active.sort(key=lambda i: i.end)
                
        # Store for future analysis
        func.analysis['spill_count'] = next_spill_slot
        
        return func
