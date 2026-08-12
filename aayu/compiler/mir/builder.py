from aayu.compiler.hir.nodes import (
    HIRModule, HIRAction, HIRAssign, HIRIf, HIRWhile,
    HIRLocal, HIRGlobal, HIRConstant, HIRBinaryOp, HIRCall
)
from aayu.compiler.mir.nodes import (
    ModuleMIR, FunctionMIR, BasicBlock, Instruction, 
    Opcode, RegisterID, Metadata, MIREnumDecl, MIREnumConstant
)

class MIRBuilder:
    def __init__(self):
        self.register_count = 0
        self.block_count = 0
        self.current_function = None
        self.current_block = None

    def _next_reg(self) -> RegisterID:
        self.register_count += 1
        return RegisterID(self.register_count)

    def _new_block(self, prefix: str = "bb") -> BasicBlock:
        self.block_count += 1
        return BasicBlock(id=f"{prefix}_{self.block_count}")

    def build(self, hir: HIRModule) -> ModuleMIR:
        functions = []
        for action in hir.actions:
            functions.append(self._build_action(action))
            
        enum_decls = []
        for e_node in getattr(hir, 'enums', []):
            enum_decls.append(MIREnumDecl(
                name=e_node.name,
                variants=[v.variant_name for v in e_node.variants],
                tags=[v.tag for v in e_node.variants],
                tag_size=e_node.tag_size
            ))
            
        struct_decls = []
        if hasattr(hir, 'structs'):
            from aayu.compiler.mir.nodes import MIRStructDecl
            for s_node in hir.structs:
                struct_decls.append(MIRStructDecl(
                    name=s_node.name,
                    fields=[f.field_type for f in s_node.fields]
                ))
            
        return ModuleMIR(functions=functions, enum_decls=enum_decls, struct_decls=struct_decls)

    def _build_action(self, action: HIRAction) -> FunctionMIR:
        self.register_count = 0
        self.block_count = 0
        
        self.current_function = FunctionMIR(name=action.name)
        entry = self._new_block("entry")
        self.current_function.blocks.append(entry)
        self.current_block = entry
        
        for stmt in action.body:
            self._build_stmt(stmt)
            
        return self.current_function

    def _build_stmt(self, stmt):
        if isinstance(stmt, HIRAssign):
            from aayu.compiler.semantic.types import StructType
            is_struct = hasattr(stmt.value, 'type_name') and isinstance(stmt.value.type_name, StructType)
            
            # For struct copy semantics, we need the pointer to the source
            if is_struct and type(stmt.value).__name__ in ("HIRLocal", "HIRGlobal", "HIRFieldAccessNode"):
                # It's an l-value, we can copy its fields
                struct_type = stmt.value.type_name
                src_ptr = self._build_lvalue(stmt.value)
                
                # Allocate new struct memory
                alloc_reg = self._next_reg()
                self.current_block.add_instruction(Instruction(
                    opcode=Opcode.ALLOC, operands=[struct_type.name], dest=alloc_reg
                ))
                
                # Copy fields
                for i, field in enumerate(struct_type.fields):
                    # Load from source
                    src_gep = self._next_reg()
                    self.current_block.add_instruction(Instruction(opcode=Opcode.GEP, operands=[src_ptr, i], dest=src_gep))
                    src_val = self._next_reg()
                    self.current_block.add_instruction(Instruction(opcode=Opcode.LOAD, operands=[src_gep], dest=src_val))
                    
                    # Store to dest
                    dst_gep = self._next_reg()
                    self.current_block.add_instruction(Instruction(opcode=Opcode.GEP, operands=[alloc_reg, i], dest=dst_gep))
                    self.current_block.add_instruction(Instruction(opcode=Opcode.STORE, operands=[src_val, dst_gep], dest=None))
                
                val_reg = alloc_reg
            else:
                val_reg = self._build_expr(stmt.value)
            
            if isinstance(stmt.target, HIRLocal):
                instr = Instruction(opcode=Opcode.STORE_LOCAL, operands=[stmt.target.name, val_reg])
            else:
                instr = Instruction(opcode=Opcode.STORE_GLOBAL, operands=[stmt.target.name, val_reg])
            
            self.current_block.add_instruction(instr)

        elif type(stmt).__name__ == "HIRFieldAssignNode":
            target_ptr_reg = self._build_lvalue(stmt.target)
            val_reg = self._build_expr(stmt.value)
            
            gep_reg = self._next_reg()
            self.current_block.add_instruction(
                Instruction(opcode=Opcode.GEP, operands=[target_ptr_reg, stmt.field_index], dest=gep_reg)
            )
            self.current_block.add_instruction(
                Instruction(opcode=Opcode.STORE, operands=[val_reg, gep_reg], dest=None)
            )

        elif isinstance(stmt, HIRCall):
            self._build_expr(stmt)

        elif type(stmt).__name__ == "HIRReturn":
            if stmt.value:
                val_reg = self._build_expr(stmt.value)
                self.current_block.add_instruction(Instruction(opcode=Opcode.RET, operands=[val_reg]))
            else:
                self.current_block.add_instruction(Instruction(opcode=Opcode.RET, operands=[]))

        elif isinstance(stmt, HIRIf):
            cond_reg = self._build_expr(stmt.condition)
            
            then_bb = self._new_block("then")
            else_bb = self._new_block("else")
            merge_bb = self._new_block("merge")
            
            # BRANCH to then or else
            branch_instr = Instruction(opcode=Opcode.BRANCH, operands=[cond_reg, then_bb.id, else_bb.id])
            self.current_block.add_instruction(branch_instr)
            
            # Link CFG
            self.current_block.successors.extend([then_bb, else_bb])
            then_bb.predecessors.append(self.current_block)
            else_bb.predecessors.append(self.current_block)
            
            self.current_function.blocks.append(then_bb)
            self.current_block = then_bb
            for t_stmt in stmt.then_branch:
                self._build_stmt(t_stmt)
            self.current_block.add_instruction(Instruction(opcode=Opcode.JUMP, operands=[merge_bb.id]))
            self.current_block.successors.append(merge_bb)
            merge_bb.predecessors.append(self.current_block)
            
            self.current_function.blocks.append(else_bb)
            self.current_block = else_bb
            if stmt.else_branch:
                for e_stmt in stmt.else_branch:
                    self._build_stmt(e_stmt)
            self.current_block.add_instruction(Instruction(opcode=Opcode.JUMP, operands=[merge_bb.id]))
            self.current_block.successors.append(merge_bb)
            merge_bb.predecessors.append(self.current_block)
            
            self.current_function.blocks.append(merge_bb)
            self.current_block = merge_bb

    def _build_expr(self, expr) -> RegisterID:
        dest = self._next_reg()
        
        if isinstance(expr, HIRConstant):
            instr = Instruction(opcode=Opcode.LOAD_CONST, operands=[expr.value], dest=dest)
            self.current_block.add_instruction(instr)
            
        elif type(expr).__name__ == "HIREnumAccessNode":
            # Preserve enum identity for downstream passes
            mir_enum = MIREnumConstant(
                enum_name=expr.enum_name,
                variant_name=expr.variant_name,
                tag=expr.tag
            )
            instr = Instruction(opcode=Opcode.LOAD_ENUM_CONST, operands=[mir_enum], dest=dest)
            self.current_block.add_instruction(instr)
            
        elif isinstance(expr, HIRLocal):
            instr = Instruction(opcode=Opcode.LOAD_LOCAL, operands=[expr.name], dest=dest)
            self.current_block.add_instruction(instr)
            
        elif isinstance(expr, HIRGlobal):
            instr = Instruction(opcode=Opcode.LOAD_GLOBAL, operands=[expr.name], dest=dest)
            self.current_block.add_instruction(instr)
            
        elif isinstance(expr, HIRBinaryOp):
            left_reg = self._build_expr(expr.left)
            right_reg = self._build_expr(expr.right)
            
            from aayu.compiler.semantic.types import StructType
            if expr.operator == '==' and isinstance(getattr(expr.left, 'type_name', None), StructType):
                struct_type = expr.left.type_name
                # Initialize result to 1 (true)
                acc_reg = self._next_reg()
                self.current_block.add_instruction(Instruction(
                    opcode=Opcode.LOAD_CONST, operands=[1], dest=acc_reg
                ))
                
                # Compare each field
                for i, field in enumerate(struct_type.fields):
                    # Get field ptr for left
                    l_gep_reg = self._next_reg()
                    self.current_block.add_instruction(Instruction(
                        opcode=Opcode.GEP, operands=[left_reg, i], dest=l_gep_reg
                    ))
                    # Load left field
                    l_val_reg = self._next_reg()
                    self.current_block.add_instruction(Instruction(
                        opcode=Opcode.LOAD, operands=[l_gep_reg], dest=l_val_reg
                    ))
                    
                    # Get field ptr for right
                    r_gep_reg = self._next_reg()
                    self.current_block.add_instruction(Instruction(
                        opcode=Opcode.GEP, operands=[right_reg, i], dest=r_gep_reg
                    ))
                    # Load right field
                    r_val_reg = self._next_reg()
                    self.current_block.add_instruction(Instruction(
                        opcode=Opcode.LOAD, operands=[r_gep_reg], dest=r_val_reg
                    ))
                    
                    # Compare fields
                    cmp_reg = self._next_reg()
                    self.current_block.add_instruction(Instruction(
                        opcode=Opcode.CMP_EQ, operands=[l_val_reg, r_val_reg], dest=cmp_reg
                    ))
                    
                    # Accumulate result with AND
                    new_acc_reg = self._next_reg() if i < len(struct_type.fields) - 1 else dest
                    self.current_block.add_instruction(Instruction(
                        opcode=Opcode.AND, operands=[acc_reg, cmp_reg], dest=new_acc_reg
                    ))
                    acc_reg = new_acc_reg
                    
                if not struct_type.fields:
                    # Empty struct, always equal
                    self.current_block.add_instruction(Instruction(
                        opcode=Opcode.MOVE, operands=[acc_reg], dest=dest
                    ))
            else:
                op_map = {
                    '+': Opcode.ADD, '-': Opcode.SUB, '*': Opcode.MUL, '/': Opcode.DIV,
                    '==': Opcode.CMP_EQ, '>': Opcode.CMP_GT, '<': Opcode.CMP_LT
                }
                opc = op_map.get(expr.operator, Opcode.ADD)
                instr = Instruction(opcode=opc, operands=[left_reg, right_reg], dest=dest)
                self.current_block.add_instruction(instr)
            
        elif isinstance(expr, HIRCall):
            arg_regs = [self._build_expr(arg) for arg in expr.args]
            # Emit LOAD_GLOBAL for function target
            func_reg = self._next_reg()
            self.current_block.add_instruction(Instruction(opcode=Opcode.LOAD_GLOBAL, operands=[expr.target], dest=func_reg))
            # Emit CALL
            call_operands = [func_reg] + arg_regs
            self.current_block.add_instruction(Instruction(opcode=Opcode.CALL, operands=call_operands, dest=dest))

        elif type(expr).__name__ == "HIRStructInitNode":
            # 1. Allocate Struct Memory (temp)
            ptr_reg = self._next_reg()
            self.current_block.add_instruction(
                Instruction(opcode=Opcode.ALLOC, operands=[expr.struct_name], dest=ptr_reg)
            )
            # 2. Assign Fields via GEP + STORE
            for i, arg_expr in enumerate(expr.args):
                arg_reg = self._build_expr(arg_expr)
                gep_reg = self._next_reg()
                self.current_block.add_instruction(
                    Instruction(opcode=Opcode.GEP, operands=[ptr_reg, i], dest=gep_reg)
                )
                self.current_block.add_instruction(
                    Instruction(opcode=Opcode.STORE, operands=[arg_reg, gep_reg], dest=None)
                )
            # 3. Load the struct value
            self.current_block.add_instruction(
                Instruction(opcode=Opcode.LOAD, operands=[ptr_reg], dest=dest)
            )

        elif type(expr).__name__ == "HIRFieldAccessNode":
            # For field access as an R-value, we first get the pointer to the target
            target_ptr_reg = self._build_lvalue(expr.target)
            gep_reg = self._next_reg()
            self.current_block.add_instruction(
                Instruction(opcode=Opcode.GEP, operands=[target_ptr_reg, expr.field_index], dest=gep_reg)
            )
            self.current_block.add_instruction(
                Instruction(opcode=Opcode.LOAD, operands=[gep_reg], dest=dest)
            )
            
        return dest
        
    def _build_lvalue(self, expr) -> RegisterID:
        """Evaluates an expression as an L-value, returning a register holding its memory pointer."""
        dest = self._next_reg()
        
        if type(expr).__name__ == "HIRLocal":
            instr = Instruction(opcode=Opcode.LOAD_LOCAL_PTR, operands=[expr.name], dest=dest)
            self.current_block.add_instruction(instr)
            return dest
            
        elif type(expr).__name__ == "HIRGlobal":
            instr = Instruction(opcode=Opcode.LOAD_GLOBAL_PTR, operands=[expr.name], dest=dest)
            self.current_block.add_instruction(instr)
            return dest
            
        elif type(expr).__name__ == "HIRFieldAccessNode":
            target_ptr_reg = self._build_lvalue(expr.target)
            self.current_block.add_instruction(
                Instruction(opcode=Opcode.GEP, operands=[target_ptr_reg, expr.field_index], dest=dest)
            )
            return dest
            
        raise NotImplementedError(f"Cannot evaluate {type(expr).__name__} as L-value")
