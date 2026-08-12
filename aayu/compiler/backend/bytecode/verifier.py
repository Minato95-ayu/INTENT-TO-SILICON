from typing import List, Tuple
from aayu.compiler.backend.bytecode.aybc import AYBCFile
from aayu.runtime.vm.instructions import Opcode

class BytecodeVerifierError(Exception):
    pass

class BytecodeVerifier:
    """Phase 14.5: Static Bytecode Verification"""
    
    def __init__(self, aybc: AYBCFile):
        self.aybc = aybc
        
    def verify(self):
        for func in self.aybc.functions:
            self._verify_function(func)
        return True
            
    def _verify_function(self, func):
        start = func.bytecode_offset
        length = func.bytecode_length
        end = start + length
        
        bytecode = self.aybc.bytecode[start:end]
        ip = 0
        
        stack_depths = {0: 0} # map of ip -> stack depth before executing instruction
        
        # We need a worklist for basic block exploration
        worklist = [(0, 0)] # (ip, current_stack)
        visited = set()
        
        while worklist:
            ip, stack = worklist.pop(0)
            
            if ip in visited:
                # If we revisit, the stack depth must match (except for polymorphic stack languages, but AAYU is strict)
                if stack_depths.get(ip, -1) != stack:
                    raise BytecodeVerifierError(f"Stack depth mismatch at IP {ip}. Expected {stack_depths.get(ip)}, got {stack}")
                continue
                
            visited.add(ip)
            stack_depths[ip] = stack
            
            if ip >= length:
                raise BytecodeVerifierError(f"Execution fell off the end of function at IP {ip}")
                
            opcode = bytecode[ip]
            
            # Predict stack changes
            push = 0
            pop = 0
            takes_arg = True
            
            if opcode in (Opcode.PUSH_CONST, Opcode.LOAD_LOCAL, Opcode.LOAD_GLOBAL, Opcode.DUP):
                push = 1
            elif opcode in (Opcode.POP, Opcode.STORE_LOCAL, Opcode.STORE_GLOBAL, Opcode.JMP_IF_FALSE):
                pop = 1
            elif opcode in (Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, 
                            Opcode.CMP_EQ, Opcode.CMP_NEQ, Opcode.CMP_LT, Opcode.CMP_GT, 
                            Opcode.CMP_LTE, Opcode.CMP_GTE):
                pop = 2
                push = 1
            elif opcode in (Opcode.JMP, Opcode.RET):
                # RET pops 1 if returning value, wait, RET assumes 1 value on stack? 
                if opcode == Opcode.RET:
                    pop = 1
            else:
                pass # Other opcodes...
                
            # Simulate stack
            next_stack = stack - pop
            if next_stack < 0:
                raise BytecodeVerifierError(f"Stack underflow at IP {ip} (Opcode {opcode:02X})")
            next_stack += push
            
            if next_stack > func.max_stack:
                raise BytecodeVerifierError(f"Stack overflow at IP {ip}. Max {func.max_stack}, got {next_stack}")
                
            # In AAYU, all current instructions take 3 bytes (1 byte opcode + 2 bytes padding/arg)
            next_ip = ip + 3
            
            # Follow control flow
            if opcode == Opcode.JMP:
                import struct
                arg = struct.unpack('>H', bytecode[ip+1:ip+3])[0]
                target = arg - start # convert absolute IP back to relative for verification
                if target < 0 or target >= length:
                    raise BytecodeVerifierError(f"JMP out of bounds to {target}")
                worklist.append((target, next_stack))
            elif opcode == Opcode.JMP_IF_FALSE:
                import struct
                arg = struct.unpack('>H', bytecode[ip+1:ip+3])[0]
                target = arg - start
                if target < 0 or target >= length:
                    raise BytecodeVerifierError(f"JMP_IF_FALSE out of bounds to {target}")
                worklist.append((target, next_stack))
                worklist.append((next_ip, next_stack))
            elif opcode == Opcode.RET:
                pass # End of path
            else:
                worklist.append((next_ip, next_stack))
                
        # Optional: check if all reachable instructions are valid
        return True
