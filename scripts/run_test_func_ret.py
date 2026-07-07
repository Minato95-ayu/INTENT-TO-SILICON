"""
=============================================================================
Test Script: Function Return Value Verification
=============================================================================
This script tests whether the AAYU compiler and virtual machine correctly
handle function return values. It processes AAYU code and traces execution
step-by-step to verify that functions return values properly.

PURPOSE:
- Load and compile AAYU source code from test_func_ret.aayu
- Execute the code line-by-line with detailed tracing
- Show the instruction pointer (IP), opcode, stack, and local variables
- Verify that function returns work correctly
=============================================================================
"""

import sys
import os

# Add the AAYU language modules to Python's path so we can import them
# These paths allow us to find the lexer, parser, compiler, and VM
sys.path.insert(0, r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\aayu_language")
sys.path.insert(0, r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype")

# Import the AAYU language processing tools
from compiler.frontend.lexer import Lexer          # Lexer: Breaks source code into tokens (like words)
from compiler.frontend.parser import Parser        # Parser: Turns tokens into an Abstract Syntax Tree (AST)
from compiler.frontend.compiler import AAYUCompiler  # Compiler: Converts AST into bytecode instructions
from vm import VirtualMachine, Frame  # VM: Executes bytecode; Frame: execution context
from opcode import Opcode        # Opcode: Instruction codes (LOAD_CONST, CALL, RETURN, etc.)

# ============================================================================
# STEP 1: Load and Compile AAYU Source Code
# ============================================================================
# This section reads the AAYU test file and compiles it into bytecode

filepath = "D:\\intent-to-silicon-research\\INTENT-TO-SILICON\\test_func_ret.aayu"
with open(filepath, 'r', encoding='utf-8') as f:
    source = f.read()  # Read the entire AAYU program as text

# STEP 1A: Lexical Analysis - Convert source code into tokens
# Example: "return 5" → [Token(RETURN), Token(INT, 5)]
lexer = Lexer(source)

# STEP 1B: Parsing - Convert tokens into an Abstract Syntax Tree (AST)
# Example: Tokens → Function definition with return statement
parser = Parser(lexer.tokenize(), filename=filepath)
ast = parser.parse()  # AST represents the program structure

# STEP 1C: Compilation - Convert AST into bytecode (like assembly for AAYU)
# Example: Return statement → [OPCODE.LOAD_CONST(5), OPCODE.RETURN]
compiler = AAYUCompiler()
code_obj = compiler.compile(ast)  # Code object contains bytecode instructions


# ============================================================================
# STEP 2: Create a Tracing Virtual Machine
# ============================================================================
# A "Tracing VM" is a version of the VM that prints each instruction it executes
# This helps us debug by seeing exactly what the program is doing step-by-step
#
# KEY CONCEPTS:
# - Instruction Pointer (IP): Points to the current instruction being executed
# - Stack: Where temporary values are stored during computation
# - Locals: Local variables in the current function
# - Call Stack: List of functions currently running (nested function calls)

class TracingVirtualMachine(VirtualMachine):
    """
    A Virtual Machine that traces (prints details of) every instruction it executes.
    Useful for debugging: you can see exactly what bytecode instructions run.
    """
    
    def run(self, code):
        """
        Execute bytecode instructions one at a time, printing details of each step.
        
        How it works:
        1. Create a Frame (execution context) for the code
        2. Add frame to call_stack (manage function calls)
        3. Loop: Execute instructions until call_stack is empty
        4. Print details before executing each instruction
        """
        frame = Frame(code)  # Create a new execution frame for this code
        self.call_stack.append(frame)  # Add frame to track nested function calls

        while self.call_stack:  # Keep running while there are frames to execute
            frame = self.call_stack[-1]  # Get the current frame (top of stack)

            # Check if we've reached the end of this frame's instructions
            if frame.ip >= len(frame.code.instructions):
                self.call_stack.pop()  # Remove this frame (function done)
                if self.call_stack:  # If there's a parent frame
                    self.call_stack[-1].stack.append(None)  # Push None as return value
                continue  # Move to next iteration

            # Get the current instruction to execute
            instruction = frame.code.instructions[frame.ip]
            
            # PRINT DEBUG INFO: Show exactly what instruction we're executing
            print(f"IP: {frame.ip:04d} | Opcode: {instruction.opcode.name:<15} | Arg: {instruction.arg}")
            print(f"    Stack : {frame.stack}")  # Show all values on the stack
            print(f"    Locals: {frame.locals}")  # Show all local variables
            
            # Extract the opcode and its argument
            opcode = instruction.opcode
            arg = instruction.arg
            
            # Move to the next instruction (increment instruction pointer)
            frame.ip += 1

            # ================================================================
            # EXECUTE INSTRUCTION: Handle each type of bytecode instruction
            # ================================================================
            
            if opcode == Opcode.LOAD_CONST:
                # LOAD_CONST: Push a constant value onto the stack
                # Example: Load the number 5 → stack becomes [5]
                frame.stack.append(arg)
                
            elif opcode == Opcode.STORE_VAR:
                # STORE_VAR: Pop top of stack and store in a variable
                # Example: stack [5] + STORE_VAR 'x' → locals['x'] = 5, stack = []
                frame.locals[arg] = frame.stack.pop()
                
            elif opcode == Opcode.LOAD_VAR:
                # LOAD_VAR: Load a variable and push it onto the stack
                # Example: locals['x'] = 5 + LOAD_VAR 'x' → stack = [5]
                if arg in frame.locals:
                    frame.stack.append(frame.locals[arg])
                else:
                    raise RuntimeError(f"Variable '{arg}' is not defined.")
                    
            elif opcode == Opcode.COMPARE_EQ:
                # COMPARE_EQ: Pop two values and check if they're equal
                # Example: stack [5, 5] + COMPARE_EQ → stack = [True]
                b = frame.stack.pop()  # Second value (right side)
                a = frame.stack.pop()  # First value (left side)
                frame.stack.append(a == b)  # Push comparison result
                
            elif opcode == Opcode.JUMP_IF_FALSE:
                # JUMP_IF_FALSE: If condition is false, jump to different instruction
                # Example: Used for if-statements: if condition is false, skip the if-block
                condition = frame.stack.pop()  # Get the condition (True or False)
                if not condition:  # If condition is false
                    frame.ip = arg  # Jump to the instruction at position 'arg'
                    
            elif opcode == Opcode.JUMP_FORWARD:
                # JUMP_FORWARD: Unconditionally jump to a different instruction
                # Example: Used to skip code or loop back
                frame.ip = arg  # Jump to the instruction at position 'arg'
                
            elif opcode == Opcode.CALL:
                # CALL: Call a function
                # The argument contains the function name and number of arguments
                func_name = arg['name']  # Which function to call
                num_args = arg['num_args']  # How many arguments it takes
                
                # Pop arguments from stack (they were pushed in reverse order)
                args = []
                for _ in range(num_args):
                    args.insert(0, frame.stack.pop())  # Insert at beginning to reverse order
                
                if func_name == 'print':
                    # Built-in print function: output the arguments
                    val = " ".join(map(str, args))
                    print(f"==> PRINT: {val}")
                    frame.stack.append(None)  # print() returns None
                else:
                    # User-defined function: look it up and execute
                    if func_name in self.globals and isinstance(self.globals[func_name], CodeObject):
                        func_code = self.globals[func_name]  # Get the function's bytecode
                        new_frame = Frame(func_code)  # Create new execution frame
                        # TODO: Need to map arguments to parameter names
                        self.call_stack.append(new_frame)  # Push new frame to call stack
                        # Note: This is where we'd set the function parameters
                    else:
                        raise RuntimeError(f"Function '{func_name}' is not defined.")
                        
            elif opcode == Opcode.RETURN:
                # RETURN: Return from current function
                # Pop value from stack (this is the return value)
                if frame.stack:
                    ret_val = frame.stack.pop()  # Get the value to return
                else:
                    ret_val = None  # If nothing on stack, return None
                    
                self.call_stack.pop()  # Pop this frame (function is done)
                
                if self.call_stack:
                    # If there's a calling function, push return value on its stack
                    self.call_stack[-1].stack.append(ret_val)
                else:
                    # If no calling function, return to caller of VM
                    return ret_val
                    
            else:
                # Unknown opcode: this shouldn't happen if the compiler works correctly
                raise RuntimeError(f"Unknown opcode: {opcode}")

# ============================================================================
# STEP 3: Run the Compiled Code with Tracing
# ============================================================================
# Now that we have the compiled bytecode, execute it using our tracing VM
# The tracing VM will print each instruction as it runs

print("=== TRACE ===")  # Print header to indicate the trace is starting

vm = TracingVirtualMachine()  # Create an instance of our tracing VM
# Set up global variables (functions and data available to all code)
# In this case, we manually add the sum_nums function for testing
vm.globals = {"sum_nums": code_obj.instructions[0].arg}

# Run the compiled code!
# This executes all the bytecode instructions while printing each step
vm.run(code_obj)
