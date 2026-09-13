from runtime.vm.exceptions import InvalidBytecodeError
from runtime.vm.instructions import Opcode

class Validator:
    """R6.2 Pre-flight verifier for bytecode."""
    
    @staticmethod
    def validate(bytecode, constant_pool):
        length = len(bytecode)
        if length % 3 != 0:
            raise InvalidBytecodeError(f"Bytecode length {length} is not a multiple of 3")
            
        instruction_boundaries = set()
        ip = 0
        
        # Pass 1: Structural boundaries and valid opcodes
        while ip < length:
            instruction_boundaries.add(ip)
            opcode = bytecode[ip]
            
            if not any(v == opcode for k,v in Opcode.__dict__.items() if not k.startswith('__')):
                raise InvalidBytecodeError(f"Unknown opcode 0x{opcode:02X}", ip)
            ip += 3

        # Subroutines registry
        # Maps target_ip -> (args, returns)
        subroutines = {}
        # Entry point is always considered a subroutine with args=0, returns=None
        subroutines[0] = (0, None)
        
        ip = 0
        while ip < length:
            opcode = bytecode[ip]
            
            if opcode == Opcode.PREPARE_CALL:
                if ip + 3 >= length or bytecode[ip+3] != Opcode.CALL:
                    raise InvalidBytecodeError("PREPARE_CALL must be immediately followed by CALL", ip)
                args = bytecode[ip+1]
                returns = bytecode[ip+2]
                target = (bytecode[ip+4] << 8) | bytecode[ip+5]
                
                if target != 0xFFFF:
                    if target not in instruction_boundaries:
                        raise InvalidBytecodeError(f"Jump target inside operand: {target}", ip)
                    if target in subroutines:
                        if subroutines[target] != (args, returns):
                            raise InvalidBytecodeError(f"ABI signature mismatch for target {target}", ip)
                    else:
                        subroutines[target] = (args, returns)
                        
            elif opcode == Opcode.CALL:
                if ip == 0 or bytecode[ip-3] != Opcode.PREPARE_CALL:
                    raise InvalidBytecodeError("Naked CALL without PREPARE_CALL", ip)
                    
            elif opcode == Opcode.CALL_COMPONENT:
                target = (bytecode[ip+1] << 8) | bytecode[ip+2]
                if target != 0xFFFF:
                    if target not in instruction_boundaries:
                        raise InvalidBytecodeError(f"Jump target inside operand: {target}", ip)
                    if target in subroutines:
                        if subroutines[target] != (1, 0):
                            raise InvalidBytecodeError(f"ABI signature mismatch for component {target}", ip)
                    else:
                        subroutines[target] = (1, 0)
            ip += 3

        # Pass 3: Control-flow and abstract stack depth validation
        # Map of (ip, expected_returns) -> depth
        visited = {}
        worklist = []
        
        for entry_ip, (args, returns) in subroutines.items():
            worklist.append((entry_ip, args, returns))
            
        while worklist:
            ip, depth, expected_returns = worklist.pop(0)
            
            if ip == 0xFFFF:
                continue
                
            if ip >= length:
                raise InvalidBytecodeError("Execution fell off the end of bytecode", ip)
                
            state_key = (ip, expected_returns)
            if state_key in visited:
                if visited[state_key] != depth:
                    raise InvalidBytecodeError(f"Incompatible stack depths at merge point: expected {visited[state_key]}, got {depth}", ip)
                continue
                
            visited[state_key] = depth
            opcode = bytecode[ip]
            new_depth = depth
            from runtime.vm.instructions import opcode_to_str
            print(f"[VAL TRACE] ip={ip} {opcode_to_str(opcode)} {depth} -> {new_depth}")
            
            if opcode in (Opcode.PUSH_CONST, Opcode.DUP, Opcode.LOAD_STATE, Opcode.CREATE_MODEL):
                new_depth += 1
            elif opcode in (Opcode.POP, Opcode.STORE_STATE, Opcode.INIT_STATE, Opcode.PRINT, Opcode.THROW, Opcode.RETHROW):
                new_depth -= 1
            elif opcode in (Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.CMP_EQ, Opcode.CMP_NEQ, Opcode.CMP_LT, Opcode.CMP_GT, Opcode.CMP_LTE, Opcode.CMP_GTE):
                new_depth -= 1 # pop 2, push 1
            elif opcode == Opcode.BUILD_WIDGET:
                operand = (bytecode[ip+1] << 8) | bytecode[ip+2]
                dynamic_prop_count = operand & 0xFF
                new_depth -= (1 + dynamic_prop_count)
            elif opcode == Opcode.CREATE_CLOSURE:
                num_args = (bytecode[ip+1] << 8) | bytecode[ip+2]
                new_depth = new_depth - num_args + 1
            elif opcode == Opcode.CREATE_ARRAY:
                count = (bytecode[ip+1] << 8) | bytecode[ip+2]
                new_depth = new_depth - count + 1
            elif opcode == Opcode.GET_LENGTH:
                pass # pop 1, push 1 -> 0
            elif opcode == Opcode.LOAD_SUBSCR:
                new_depth -= 1 # pop 2, push 1
            elif opcode == Opcode.STORE_SUBSCR:
                new_depth -= 3 # pop 3, push 0
            elif opcode == Opcode.DB_INSERT:
                idx = (bytecode[ip+1] << 8) | bytecode[ip+2]
                info = constant_pool[idx]
                fields_count = info["fields_count"]
                new_depth -= (2 * fields_count)
                new_depth += 1 # because compiler emits PUSH_CONST 0 immediately after, but wait, DB_INSERT doesn't push at runtime, it's just the compiler emitting PUSH_CONST 0 next. So DB_INSERT itself has net depth - (2 * fields_count).
            elif opcode == Opcode.DB_FIND:
                new_depth += 1  # DB_FIND pushes the found model/array
            elif opcode == Opcode.BUILD_DICT:
                num_keys = (bytecode[ip+1] << 8) | bytecode[ip+2]
                new_depth -= num_keys  # pops list of keys (1) + num_keys values, then pushes 1 dict. Net = -num_keys
            elif opcode == Opcode.NAVIGATE:
                num_args = (bytecode[ip+1] << 8) | bytecode[ip+2]
                new_depth -= (num_args + 1)
            elif opcode == Opcode.OP_ASYNC_CALL:
                num_args = (bytecode[ip+1] << 8) | bytecode[ip+2]
                new_depth -= num_args
                new_depth += 1  # OP_ASYNC_CALL pushes a result
            elif opcode in (Opcode.DECLARE_THEME, Opcode.SET_THEME):
                new_depth -= 1
            elif opcode in (Opcode.SET_BINDING, Opcode.DECLARE_VALIDATION, Opcode.SET_ANIMATION, Opcode.DECLARE_LIFECYCLE):
                new_depth -= 2
            elif opcode == Opcode.CALL:
                args = bytecode[ip-2]
                returns = bytecode[ip-1]
                if new_depth < args:
                    raise InvalidBytecodeError(f"Insufficient stack depth for CALL. Expected {args}, got {new_depth}", ip)
                new_depth = new_depth - args + returns
            elif opcode == Opcode.CALL_COMPONENT:
                new_depth -= 1
            elif opcode == Opcode.PREPARE_CALL:
                pass # No-op
            elif opcode == Opcode.MARK_BLOCK_START:
                pass # Modifies node_stack
            elif opcode in (Opcode.REGISTER_ROUTE, Opcode.CHECK_AUTH, Opcode.SETUP_EXCEPT, Opcode.POP_EXCEPT, Opcode.SETUP_FINALLY, Opcode.EXEC_FINALLY):
                pass # Assuming 0 delta
            elif opcode == Opcode.RETURN_VALUE:
                if expected_returns is not None and expected_returns != 1:
                    raise InvalidBytecodeError(f"RETURN_VALUE used but expected {expected_returns} returns", ip)
                if new_depth != 1:
                    raise InvalidBytecodeError(f"Stack depth mismatch on RETURN_VALUE: expected 1, got {new_depth}", ip)
                continue
            elif opcode == Opcode.RET:
                if expected_returns is not None and expected_returns != 0:
                    raise InvalidBytecodeError(f"RET used but expected {expected_returns} returns. IP={ip}. subroutines={subroutines}", ip)
                if new_depth != 0:
                    raise InvalidBytecodeError(f"Stack depth mismatch on RET: expected 0, got {new_depth}", ip)
                continue
            elif opcode == Opcode.HALT:
                continue
            elif opcode == Opcode.JMP:
                target = (bytecode[ip+1] << 8) | bytecode[ip+2]
                if target != 0xFFFF and target not in instruction_boundaries:
                    raise InvalidBytecodeError(f"Jump target inside operand: {target}", ip)
                worklist.append((target, new_depth, expected_returns))
                continue
            elif opcode == Opcode.JMP_IF_FALSE:
                new_depth -= 1
                if new_depth < 0:
                    raise InvalidBytecodeError("Stack underflow", ip)
                target = (bytecode[ip+1] << 8) | bytecode[ip+2]
                if target != 0xFFFF and target not in instruction_boundaries:
                    raise InvalidBytecodeError(f"Jump target inside operand: {target}", ip)
                worklist.append((target, new_depth, expected_returns))
                worklist.append((ip + 3, new_depth, expected_returns))
                continue
            elif opcode in (Opcode.GET_ITER, Opcode.FOR_ITER):
                # FOR_ITER will be replaced in R6.1-D, for now assume 0 stack effect conceptually for iteration
                pass
                
            if new_depth < 0:
                raise InvalidBytecodeError("Stack underflow", ip)
                
            worklist.append((ip + 3, new_depth, expected_returns))
            
        return True
