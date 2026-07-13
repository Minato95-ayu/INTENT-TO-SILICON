from typing import List, Tuple, Any
from dataclasses import dataclass, field
from compiler.ir.lir import LIRNode
from compiler.bytecode.constant_pool import ConstantPool
from compiler.bytecode.header import BinaryHeader
from runtime.vm.instructions import Opcode

# Widget type indices for BUILD_WIDGET operand
WIDGET_TYPES = {
    "TEXT": 0,
    "BUTTON": 1,
    "CONTAINER": 2,
    "IMAGE": 3,
    "ROW": 4,
    "COLUMN": 5,
    "CARD": 6,
    "INPUT": 7,
    "PAGE": 8,
}

@dataclass
class Relocation:
    """A relocation entry for future jump patching."""
    offset: int       # byte offset in the instruction stream
    symbol: str       # target label/action name
    type: str = "JUMP"  # relocation type

@dataclass
class EncodedProgram:
    """The complete encoded bytecode output."""
    header: BinaryHeader
    bytecode: bytearray
    constant_pool: ConstantPool
    relocation_table: List[Relocation] = field(default_factory=list)


class BytecodeEncoder:
    """Encodes LIR nodes into fixed-width binary bytecode.
    
    Instruction format: 3 bytes each
        [OPCODE: 1 byte] [OPERAND: 2 bytes big-endian]
    
    Opcodes without operands use 0x0000 as padding.
    """

    INSTRUCTION_WIDTH = 3  # 1 byte opcode + 2 byte operand

    def __init__(self):
        self.pool = ConstantPool()
        self.bytecode = bytearray()
        self.relocations: List[Relocation] = []
        self._action_addresses: dict = {}  # action_name -> bytecode offset

    def encode(self, lir_nodes: List[LIRNode]) -> EncodedProgram:
        """Encode a list of LIR nodes into a complete binary program."""
        self.pool = ConstantPool()
        self.bytecode = bytearray()
        self.relocations = []
        self._action_addresses = {}

        # Two-pass encoding:
        # Pass 1: Collect action addresses (for CALL resolution)
        # Pass 2: Emit bytecode

        # Pass 1: pre-scan for action declarations to get their addresses
        fake_offset = 0
        for node in lir_nodes:
            if node.opcode == "ACTION_DECL":
                action_name = node.operands[0]
                # The action body will start after a JMP over it
                # We'll handle this in pass 2
            fake_offset += self._estimate_size(node)

        # Pass 2: emit actual bytecode
        for node in lir_nodes:
            self._encode_node(node)

        # Append HALT
        self._emit(Opcode.HALT, 0)

        # Build header
        instruction_count = len(self.bytecode) // self.INSTRUCTION_WIDTH
        header = BinaryHeader(
            version_major=1,
            version_minor=0,
            instruction_count=instruction_count,
            constant_pool_size=self.pool.size(),
            flags=0
        )

        return EncodedProgram(
            header=header,
            bytecode=self.bytecode,
            constant_pool=self.pool,
            relocation_table=self.relocations
        )

    def _emit(self, opcode: int, operand: int = 0):
        """Emit a single 3-byte instruction."""
        self.bytecode.append(opcode & 0xFF)
        self.bytecode.append((operand >> 8) & 0xFF)
        self.bytecode.append(operand & 0xFF)

    def _encode_node(self, node: LIRNode):
        """Dispatch a single LIR node to the appropriate encoder."""
        opcode = node.opcode

        if opcode == "STATE_INIT":
            self._encode_state_init(node)
        elif opcode == "LOAD_VAR":
            self._encode_load_var(node)
        elif opcode == "STORE_VAR":
            self._encode_store_var(node)
        elif opcode.startswith("BUILD_"):
            self._encode_build_widget(node)
        elif opcode == "PRINT":
            self._encode_print(node)
        elif opcode == "PRINT_STACK":
            # Value is already on stack — just emit PRINT
            self._emit(Opcode.PRINT, 0)
        elif opcode == "PUSH_CONST":
            self._encode_push_const(node)
        elif opcode == "ACTION_DECL":
            self._encode_action_decl(node)
        elif opcode == "CALL_ACTION":
            self._encode_call_action(node)
        elif opcode == "ADD":
            self._emit(Opcode.ADD, 0)
        elif opcode == "SUB":
            self._emit(Opcode.SUB, 0)
        elif opcode == "MUL":
            self._emit(Opcode.MUL, 0)
        elif opcode == "DIV":
            self._emit(Opcode.DIV, 0)
        elif opcode == "POP":
            self._emit(Opcode.POP, 0)
        elif opcode == "NOP":
            pass  # skip no-ops
        else:
            # Unknown LIR opcode — emit as DISPATCH for extensibility
            self._emit(Opcode.DISPATCH, 0)

    def _encode_state_init(self, node: LIRNode):
        """STATE_INIT [name, initial_value]
        → PUSH_CONST value_idx
        → STORE_STATE name_idx
        """
        name = node.operands[0]
        value = node.operands[1]

        value_idx = self.pool.add(value)
        name_idx = self.pool.add(name)

        self._emit(Opcode.PUSH_CONST, value_idx)
        self._emit(Opcode.STORE_STATE, name_idx)

    def _encode_load_var(self, node: LIRNode):
        """LOAD_VAR [name] → LOAD_STATE name_idx"""
        name = node.operands[0]
        name_idx = self.pool.add(name)
        self._emit(Opcode.LOAD_STATE, name_idx)

    def _encode_store_var(self, node: LIRNode):
        """STORE_VAR [name] → STORE_STATE name_idx"""
        name = node.operands[0]
        name_idx = self.pool.add(name)
        self._emit(Opcode.STORE_STATE, name_idx)

    def _encode_build_widget(self, node: LIRNode):
        """BUILD_* [props] → PUSH_CONST content + BUILD_WIDGET type
        
        The widget type is derived from the LIR opcode suffix.
        Props on the stack, widget type as operand.
        """
        # Extract widget type from opcode: BUILD_TEXT -> TEXT
        widget_type_str = node.opcode[6:]  # strip "BUILD_"
        widget_type_id = WIDGET_TYPES.get(widget_type_str, 0)

        # Push widget content/props onto stack
        props = node.operands[0] if node.operands else {}
        if isinstance(props, dict):
            # For widgets with text content, push the text
            text = props.get("text", props.get("title", props.get("name", "")))
            if text:
                text_idx = self.pool.add(str(text))
                self._emit(Opcode.PUSH_CONST, text_idx)
            else:
                # Push empty string for widgets without text content
                empty_idx = self.pool.add("")
                self._emit(Opcode.PUSH_CONST, empty_idx)
        elif isinstance(props, str):
            text_idx = self.pool.add(props)
            self._emit(Opcode.PUSH_CONST, text_idx)
        else:
            empty_idx = self.pool.add("")
            self._emit(Opcode.PUSH_CONST, empty_idx)

        self._emit(Opcode.BUILD_WIDGET, widget_type_id)

    def _encode_print(self, node: LIRNode):
        """PRINT [value] → PUSH_CONST value_idx + PRINT"""
        if node.operands:
            value = node.operands[0]
            value_idx = self.pool.add(value)
            self._emit(Opcode.PUSH_CONST, value_idx)
        self._emit(Opcode.PRINT, 0)

    def _encode_push_const(self, node: LIRNode):
        """PUSH_CONST [value] → PUSH_CONST idx"""
        value = node.operands[0]
        idx = self.pool.add(value)
        self._emit(Opcode.PUSH_CONST, idx)

    def _encode_action_decl(self, node: LIRNode):
        """ACTION_DECL [name, body_lir_nodes]
        Actions are stored and called via CALL.
        For RC1, we record the address for later CALL resolution.
        """
        action_name = node.operands[0]
        self._action_addresses[action_name] = len(self.bytecode)

        # Encode body statements
        if len(node.operands) > 1:
            body_nodes = node.operands[1]
            if isinstance(body_nodes, list):
                for sub_node in body_nodes:
                    if isinstance(sub_node, LIRNode):
                        self._encode_node(sub_node)

        # Return from action
        self._emit(Opcode.RET, 0)

    def _encode_call_action(self, node: LIRNode):
        """CALL_ACTION [name] → CALL target_address"""
        action_name = node.operands[0]
        if action_name in self._action_addresses:
            target = self._action_addresses[action_name]
            self._emit(Opcode.CALL, target)
        else:
            # Forward reference — add relocation
            self.relocations.append(Relocation(
                offset=len(self.bytecode),
                symbol=action_name,
                type="CALL"
            ))
            self._emit(Opcode.CALL, 0xFFFF)  # placeholder

    def _estimate_size(self, node: LIRNode) -> int:
        """Estimate byte size of a LIR node for pre-scanning."""
        opcode = node.opcode
        if opcode == "STATE_INIT":
            return 6  # PUSH_CONST + STORE_STATE
        elif opcode.startswith("BUILD_"):
            return 6  # PUSH_CONST + BUILD_WIDGET
        elif opcode == "PRINT":
            return 6  # PUSH_CONST + PRINT
        elif opcode == "ACTION_DECL":
            return 3  # RET only (body nodes counted separately)
        else:
            return 3  # single instruction
