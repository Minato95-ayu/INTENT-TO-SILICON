from typing import Dict, List, Tuple
from aayu.compiler.mir.nodes import FunctionMIR, Instruction, Opcode, RegisterID
from aayu.compiler.pass_manager import OptimizationPass
from aayu.compiler.backend.registers import LiveInterval, PhysicalRegister, RegisterClass

class SpillSlotManager:
    def __init__(self):
        self.slots = {}
        self.max_slot = 0
        
    def allocate(self, interval_id: int) -> int:
        if interval_id not in self.slots:
            self.slots[interval_id] = self.max_slot
            self.max_slot += 1
        return self.slots[interval_id]

class SpillRewritePass(OptimizationPass):
    """
    Rewrites MIR instructions to use LOAD_SPILL and STORE_SPILL for spilled registers.
    Uses reserved temporary registers.
    """
    
    def __init__(self):
        # Dedicated scratch registers for spills
        self.scratch_regs = [
            PhysicalRegister(id=900, name="tmp0", kind=RegisterClass.GENERAL, width=64, reserved=True),
            PhysicalRegister(id=901, name="tmp1", kind=RegisterClass.GENERAL, width=64, reserved=True),
            PhysicalRegister(id=902, name="tmp2", kind=RegisterClass.GENERAL, width=64, reserved=True)
        ]
        
    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not func.blocks:
            return func
            
        if not hasattr(func, 'analysis') or 'intervals' not in func.analysis:
            raise Exception("Live Intervals required for Spill Rewrite.")
            
        intervals: Dict[int, LiveInterval] = func.analysis['intervals']
        
        # Determine spilled intervals
        spilled_intervals = {k: v for k, v in intervals.items() if v.assigned_register is None and v.spill_slot is not None}
        
        if not spilled_intervals:
            # No spills, nothing to rewrite!
            func.analysis['spills'] = 0
            func.analysis['reloads'] = 0
            func.analysis['stack_slots'] = 0
            return func
            
        spill_manager = SpillSlotManager()
        
        # Populate spill manager
        for interval in spilled_intervals.values():
            spill_manager.allocate(interval.register_id)
            
        total_spills = 0
        total_reloads = 0
        
        # We need to create LOAD_SPILL and STORE_SPILL opcodes
        load_spill_op = Opcode.LOAD_SPILL
        store_spill_op = Opcode.STORE_SPILL
        
        for block in func.blocks:
            new_instructions = []
            
            for instr in block.instructions:
                # If PHI node, we technically shouldn't see spilled registers in PHI directly here
                # because we are transforming MIR to LIR. 
                # But for now, handle generic instructions.
                
                scratch_idx = 0
                load_instrs = []
                store_instrs = []
                
                # 1. Handle Operands (Reads)
                new_operands = []
                for op in instr.operands:
                    if isinstance(op, RegisterID) and op.id in spilled_intervals:
                        slot = spill_manager.slots[op.id]
                        tmp_reg = self.scratch_regs[scratch_idx]
                        scratch_idx += 1
                        
                        # Emit LOAD_SPILL tmp, slot
                        # We use RegisterID to wrap physical registers for now in MIR
                        tmp_rid = RegisterID(id=tmp_reg.id)
                        load_instrs.append(
                            Instruction(load_spill_op, [slot], dest=tmp_rid, index=instr.index - 1)
                        )
                        new_operands.append(tmp_rid)
                        total_reloads += 1
                    else:
                        new_operands.append(op)
                        
                instr.operands = new_operands
                
                # 2. Handle Destination (Writes)
                if instr.dest and instr.dest.id in spilled_intervals:
                    slot = spill_manager.slots[instr.dest.id]
                    tmp_reg = self.scratch_regs[scratch_idx]
                    scratch_idx += 1
                    
                    tmp_rid = RegisterID(id=tmp_reg.id)
                    original_dest = instr.dest
                    instr.dest = tmp_rid
                    
                    # Emit STORE_SPILL slot, tmp
                    store_instrs.append(
                        Instruction(store_spill_op, [slot, tmp_rid], dest=None, index=instr.index + 1)
                    )
                    total_spills += 1
                    
                # 3. Assemble sequence
                new_instructions.extend(load_instrs)
                new_instructions.append(instr)
                new_instructions.extend(store_instrs)
                
            block.instructions = new_instructions
            
        # Store metrics
        func.analysis['spills'] = total_spills
        func.analysis['reloads'] = total_reloads
        func.analysis['stack_slots'] = spill_manager.max_slot
        
        return func
