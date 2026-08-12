from typing import List
import struct
class Opcode: pass
from aayu.compiler.backend.bytecode.aybc import AYBCFile, FunctionMetadata, TypeTag, MAGIC_BYTES, VERSION, FLAGS
from aayu.compiler.backend.bytecode.lowering import StackInstruction

class BytecodeEmitter:
    def __init__(self):
        self.aybc = AYBCFile()
        self.bytecode = bytearray()
        
    def emit_function(self, name: str, instructions: List[StackInstruction], locals_count: int, max_stack: int):
        name_idx = self.aybc.add_constant(name)
        
        # We need 2 passes for jumps
        # Pass 1: find offsets for all labels
        label_offsets = {}
        current_offset = 0
        
        for instr in instructions:
            if instr.label is not None:
                label_offsets[instr.label] = current_offset
            else:
                # Instruction takes space.
                # opcode is 1 byte.
                # If it has an arg (JMP, LOAD_LOCAL, PUSH_CONST, etc.), it takes +2 bytes (fetch16).
                # Some opcodes like ADD, POP, SUB don't take args in the encoded format.
                if self._takes_arg(instr.opcode):
                    current_offset += 3
                else:
                    current_offset += 3 # WAIT, interpreter.py hardcodes `self.vm.registers.ip += 3` for EVERYTHING! Let's check:
                    # Oh, looking at `interpreter.py`, even `Opcode.POP` does `self.vm.registers.ip += 3`!
                    # And `ADD` does `ip += 3`!
                    # So ALL instructions in AAYU VM currently take 3 bytes! (opcode + 2 bytes padding/arg).
                    # current_offset += 3 is consistent with the current VM!
                    
        # Pass 2: emit bytes
        start_offset = len(self.bytecode)
        
        for instr in instructions:
            if instr.label is not None:
                continue
                
            self.bytecode.append(instr.opcode)
            
            arg_val = 0
            if instr.opcode == Opcode.PUSH_CONST:
                arg_val = self.aybc.add_constant(instr.arg)
            elif instr.opcode in (Opcode.LOAD_LOCAL, Opcode.STORE_LOCAL):
                arg_val = instr.arg
            elif instr.opcode in (Opcode.JMP, Opcode.JMP_IF_FALSE):
                # The target is the absolute IP of the label.
                # start_offset is where this function starts in the global bytecode.
                target_offset = start_offset + label_offsets[instr.arg]
                arg_val = target_offset
            
            # Pack the 16-bit argument (or padding)
            self.bytecode.extend(struct.pack('>H', arg_val))
            
        end_offset = len(self.bytecode)
        
        func_meta = FunctionMetadata(
            name_index=name_idx,
            locals_count=locals_count,
            parameter_count=0, # To be implemented
            max_stack=max_stack,
            bytecode_offset=start_offset,
            bytecode_length=end_offset - start_offset
        )
        self.aybc.functions.append(func_meta)
        
    def _takes_arg(self, opcode: int) -> bool:
        # In current interpreter.py, EVERYTHING advances IP by 3.
        # So we can just return True.
        return True
        
    def generate(self) -> bytes:
        out = bytearray()
        
        # Header
        out.extend(MAGIC_BYTES)
        out.extend(struct.pack('<H', VERSION))
        out.extend(struct.pack('<H', FLAGS))
        
        out.extend(struct.pack('<I', len(self.aybc.constants)))
        out.extend(struct.pack('<I', len(self.aybc.functions)))
        
        # Constant Pool
        for const in self.aybc.constants:
            if isinstance(const, int):
                out.append(TypeTag.INTEGER)
                out.extend(struct.pack('<q', const)) # 64-bit int
            elif isinstance(const, float):
                out.append(TypeTag.FLOAT)
                out.extend(struct.pack('<d', const)) # 64-bit float
            elif isinstance(const, bool):
                out.append(TypeTag.BOOLEAN)
                out.append(1 if const else 0)
            elif const is None:
                out.append(TypeTag.NULL)
            elif isinstance(const, str):
                out.append(TypeTag.STRING)
                encoded = const.encode('utf-8')
                out.extend(struct.pack('<I', len(encoded)))
                out.extend(encoded)
            else:
                raise ValueError(f"Unsupported constant type {type(const)}")
                
        # Function Table
        for func in self.aybc.functions:
            out.extend(struct.pack('<I', func.name_index))
            out.extend(struct.pack('<I', func.locals_count))
            out.extend(struct.pack('<I', func.parameter_count))
            out.extend(struct.pack('<I', func.max_stack))
            out.extend(struct.pack('<I', func.bytecode_offset))
            out.extend(struct.pack('<I', func.bytecode_length))
            
        # Bytecode Section
        self.aybc.bytecode = self.bytecode
        out.extend(self.bytecode)
        
        return bytes(out)
