from typing import Dict, List, Set, Any
from aayu.compiler.mir.nodes import FunctionMIR, Instruction, Opcode, RegisterID
from aayu.compiler.pass_manager import OptimizationPass
import copy

class SSARenamerPass(OptimizationPass):
    """
    Renames local variables to SSA RegisterIDs and removes LOAD_LOCAL / STORE_LOCAL.
    Traverses the Dominator Tree to assign versions and wire PHI node edges.
    """
    def __init__(self):
        self.var_stacks: Dict[str, List[RegisterID]] = {}
        self.register_alias: Dict[int, RegisterID] = {}
        self.max_reg_id = 0

    def _next_reg(self) -> RegisterID:
        self.max_reg_id += 1
        return RegisterID(self.max_reg_id)

    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not hasattr(func, 'analysis') or 'dom_tree' not in func.analysis:
            raise Exception("Dominator Tree not found. Run DominatorTreePass first.")
            
        self.var_stacks.clear()
        self.register_alias.clear()
        
        # Find max register ID to allocate fresh ones
        self.max_reg_id = 0
        for b in func.blocks:
            for instr in b.instructions:
                if instr.dest and instr.dest.id > self.max_reg_id:
                    self.max_reg_id = instr.dest.id
                for op in instr.operands:
                    if isinstance(op, RegisterID) and op.id > self.max_reg_id:
                        self.max_reg_id = op.id

        dom_tree = func.analysis['dom_tree']
        
        if func.blocks:
            self._rename_block(func, func.entry_block.id, dom_tree)
            
        # Cleanup removed instructions (LOAD_LOCAL, STORE_LOCAL)
        for b in func.blocks:
            new_instrs = []
            for instr in b.instructions:
                if instr.opcode not in (Opcode.LOAD_LOCAL, Opcode.STORE_LOCAL):
                    # Also replace any aliases in operands
                    new_operands = []
                    for op in instr.operands:
                        if isinstance(op, RegisterID):
                            new_operands.append(self._resolve_alias(op))
                        elif instr.opcode == Opcode.PHI and isinstance(op, list):
                            # PHI operands are already processed nicely, but let's just make sure inner aliases are resolved
                            resolved_edges = []
                            for pred_id, val in op:
                                if isinstance(val, RegisterID):
                                    resolved_edges.append((pred_id, self._resolve_alias(val)))
                                else:
                                    resolved_edges.append((pred_id, val))
                            new_operands.append(resolved_edges)
                        else:
                            new_operands.append(op)
                    
                    instr.operands = new_operands
                    if instr.opcode == Opcode.PHI:
                        # Flatten operands list for PHI
                        # Current: operands = [[(Block1, r1), (Block2, r2)]]
                        # Target: operands = [(Block1, r1), (Block2, r2)]
                        if len(instr.operands) == 1 and isinstance(instr.operands[0], list):
                            instr.operands = instr.operands[0]
                            
                    new_instrs.append(instr)
            b.instructions = new_instrs

        return func

    def _resolve_alias(self, reg: RegisterID) -> RegisterID:
        curr = reg
        while curr.id in self.register_alias:
            curr = self.register_alias[curr.id]
        return curr

    def _rename_block(self, func: FunctionMIR, block_id: str, dom_tree: Dict[str, List[str]]):
        block = next(b for b in func.blocks if b.id == block_id)
        
        pushed_vars: Dict[str, int] = {} # Count of how many times a var was pushed in this block
        
        # 1. Process PHI nodes
        for instr in block.instructions:
            if instr.opcode == Opcode.PHI:
                # var_name may be in operands[0] if uninitialized, or in _var_name if a predecessor visited already
                var_name = getattr(instr, '_var_name', instr.operands[0])
                new_dest = self._next_reg()
                instr.dest = new_dest
                
                if var_name not in self.var_stacks:
                    self.var_stacks[var_name] = []
                self.var_stacks[var_name].append(new_dest)
                pushed_vars[var_name] = pushed_vars.get(var_name, 0) + 1
                
                if not hasattr(instr, '_var_name'):
                    instr._var_name = var_name
                    instr.operands = [[]]

        # 2. Process normal instructions
        for instr in block.instructions:
            if instr.opcode == Opcode.LOAD_LOCAL:
                var_name = instr.operands[0]
                dest_reg = instr.dest
                # Aliasing: dest_reg is now an alias for the top of the stack
                if var_name in self.var_stacks and self.var_stacks[var_name]:
                    self.register_alias[dest_reg.id] = self.var_stacks[var_name][-1]
                else:
                    # Undefined variable usage (should be caught by semantic, but just in case)
                    pass
                    
            elif instr.opcode == Opcode.STORE_LOCAL:
                var_name = instr.operands[0]
                val_reg = instr.operands[1]
                val_reg = self._resolve_alias(val_reg)
                
                if var_name not in self.var_stacks:
                    self.var_stacks[var_name] = []
                self.var_stacks[var_name].append(val_reg)
                pushed_vars[var_name] = pushed_vars.get(var_name, 0) + 1

        # 3. Fill in PHI operands in successors
        for succ in block.successors:
            for instr in succ.instructions:
                if instr.opcode == Opcode.PHI:
                    var_name = getattr(instr, '_var_name', None)
                    if not var_name and len(instr.operands) > 0 and isinstance(instr.operands[0], str):
                        var_name = instr.operands[0]
                        
                    if var_name and var_name in self.var_stacks and self.var_stacks[var_name]:
                        top_reg = self.var_stacks[var_name][-1]
                        
                        # Initialize the operands array if we haven't processed this PHI node yet
                        if not hasattr(instr, '_var_name'):
                            instr._var_name = var_name
                            instr.operands = [[]]
                            
                        instr.operands[0].append((block.id, top_reg))

        # 4. Recursively visit children in dominator tree
        for child_id in dom_tree.get(block_id, []):
            self._rename_block(func, child_id, dom_tree)

        # 5. Pop stacks
        for var_name, count in pushed_vars.items():
            for _ in range(count):
                self.var_stacks[var_name].pop()
