from typing import List, Any
from runtime.vm.instructions import Opcode, opcode_to_str

# Opcodes that reference the constant pool
_POOL_REF_OPCODES = {Opcode.PUSH_CONST, Opcode.STORE_STATE, Opcode.LOAD_STATE}

# Widget type names
_WIDGET_TYPES = {
    0: "TEXT", 1: "BUTTON", 2: "CONTAINER", 3: "IMAGE",
    4: "ROW", 5: "COLUMN", 6: "CARD", 7: "INPUT", 8: "PAGE",
}

INSTRUCTION_WIDTH = 3


def disassemble(bytecode: bytearray, constant_pool: List[Any] = None) -> str:
    """Disassemble raw bytecode into human-readable assembly.
    
    Output format:
        OFFSET  OPCODE_NAME  OPERAND  [; comment]
    
    Example:
        0000  PUSH_CONST     0       ; = 42
        0003  STORE_STATE    1       ; = "counter"
        0006  HALT           0
    """
    lines = []
    ip = 0
    length = len(bytecode)

    while ip + 2 < length:
        opcode = bytecode[ip]
        operand = (bytecode[ip + 1] << 8) | bytecode[ip + 2]

        name = opcode_to_str(opcode)
        comment = ""

        # Add constant pool value as comment
        if opcode in _POOL_REF_OPCODES and constant_pool and operand < len(constant_pool):
            val = constant_pool[operand]
            comment = f"; = {val!r}"

        # Add widget type name as comment
        if opcode == Opcode.BUILD_WIDGET:
            wt = _WIDGET_TYPES.get(operand, "UNKNOWN")
            comment = f"; type={wt}"

        # Add jump/call target as comment
        if opcode in (Opcode.JMP, Opcode.JMP_IF_FALSE, Opcode.CALL):
            if operand == 0xFFFF:
                comment = "; UNRESOLVED"
            else:
                comment = f"; -> {operand:04d}"

        line = f"{ip:04d}  {name:<16s} {operand:<6d} {comment}"
        lines.append(line.rstrip())

        ip += INSTRUCTION_WIDTH

    # Handle any remaining bytes (shouldn't happen with valid bytecode)
    if ip < length:
        remaining = bytecode[ip:]
        lines.append(f"{ip:04d}  <{len(remaining)} trailing bytes>")

    return "\n".join(lines)


def disassemble_with_header(bytecode: bytearray, constant_pool: List[Any] = None,
                             header=None) -> str:
    """Full disassembly including header and constant pool dump."""
    sections = []

    # Header section
    if header:
        sections.append(f"=== AAYU Bytecode v{header.version_major}.{header.version_minor} ===")
        sections.append(f"Instructions: {header.instruction_count}")
        sections.append(f"Constants:    {header.constant_pool_size}")
        sections.append(f"Flags:        0x{header.flags:04X}")
        sections.append("")

    # Constant pool section
    if constant_pool:
        sections.append("--- Constant Pool ---")
        for i, val in enumerate(constant_pool):
            type_name = type(val).__name__.upper()
            if isinstance(val, bool):
                type_name = "BOOL"
            elif isinstance(val, int):
                type_name = "INT"
            elif isinstance(val, float):
                type_name = "FLOAT"
            elif isinstance(val, str):
                type_name = "STRING"
            sections.append(f"  {i:4d}  {type_name:8s}  {val!r}")
        sections.append("")

    # Instruction section
    sections.append("--- Instructions ---")
    sections.append(disassemble(bytecode, constant_pool))

    return "\n".join(sections)
