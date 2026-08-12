from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum, auto

class CallingConvType(Enum):
    AAYU_BYTECODE = auto() # Virtual machine calling convention
    CDECL = auto()         # Standard C
    SYSTEM_V = auto()      # Linux/macOS x64
    WIN64 = auto()         # Windows x64
    WASM = auto()          # WebAssembly

@dataclass
class CallingConvention:
    conv_type: CallingConvType
    
    # Registers used for passing arguments (in order)
    arg_registers: List[str] = field(default_factory=list)
    
    # Registers used for returning values
    return_registers: List[str] = field(default_factory=list)
    
    # Registers that the callee must preserve
    callee_saved: List[str] = field(default_factory=list)
    
    # Registers that the caller must preserve
    caller_saved: List[str] = field(default_factory=list)
    
    # Alignment required for the stack pointer (bytes)
    stack_alignment: int = 16 

# Pre-defined constraints
SystemV_x64 = CallingConvention(
    conv_type=CallingConvType.SYSTEM_V,
    arg_registers=["rdi", "rsi", "rdx", "rcx", "r8", "r9"],
    return_registers=["rax", "rdx"],
    callee_saved=["rbx", "rbp", "r12", "r13", "r14", "r15"],
    caller_saved=["rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"],
    stack_alignment=16
)

Win64 = CallingConvention(
    conv_type=CallingConvType.WIN64,
    arg_registers=["rcx", "rdx", "r8", "r9"],
    return_registers=["rax"],
    callee_saved=["rbx", "rbp", "rdi", "rsi", "r12", "r13", "r14", "r15"],
    caller_saved=["rax", "rcx", "rdx", "r8", "r9", "r10", "r11"],
    stack_alignment=16
)

AayuBytecodeCC = CallingConvention(
    conv_type=CallingConvType.AAYU_BYTECODE,
    # The Bytecode VM passes everything on the eval stack, no physical registers
    arg_registers=[],
    return_registers=[],
    callee_saved=[],
    caller_saved=[],
    stack_alignment=1 # Irrelevant for VM
)
