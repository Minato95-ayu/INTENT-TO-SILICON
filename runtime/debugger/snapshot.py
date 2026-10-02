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

import copy

class VMSnapshot:
    """Immutable snapshot of the VM state when paused."""
    def __init__(self, vm):
        # We deeply copy or extract primitive state to prevent live mutation
        self.ip = vm.registers.ip
        self.registers = copy.deepcopy(vm.registers.__dict__)
        
        # Snapshot the call stack (just frames)
        self.call_stack = []
        for frame in vm.call_stack.frames:
            self.call_stack.append({
                "function": frame.function_name,
                "ip": frame.return_address,
                "locals": copy.deepcopy(frame.locals)
            })
            
        # Optional: Heap snapshot summary
        self.heap_summary = {
            "allocated": len(vm.heap.allocator.pool.pool)
        }
