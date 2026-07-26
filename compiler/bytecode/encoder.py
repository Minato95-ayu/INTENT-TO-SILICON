from typing import List, Tuple, Any
from dataclasses import dataclass, field
from compiler.ir.lir import LIRNode
from compiler.bytecode.constant_pool import ConstantPool
from compiler.bytecode.header import BinaryHeader
from runtime.vm.instructions import Opcode

# Widget type indices for BUILD_WIDGET operand
WIDGET_TYPES = {
    "PAGE": 1,
    "COLUMN": 2,
    "ROW": 3,
    "CONTAINER": 4,
    "CARD": 5,
    "TEXT": 6,
    "HEADING": 7,
    "BUTTON": 8,
    "INPUT": 9,
    "IMAGE": 10,
    "STACK": 11,
    "PADDING": 12,
    "MARGIN": 13,
    "ALIGN": 14,
    "EXPANDED": 15,
    "SPACER": 16,
    "ICON": 17,
    "COMPONENT": 18,
    "LIST": 19,
    "GRID": 20,
    "CENTER": 21,
    "DIVIDER": 22,
    "SCROLLVIEW": 23,
    "APPBAR": 24,
    "NAVIGATIONBAR": 25,
    "DRAWER": 26,
    "DIALOG": 27,
    "SNACKBAR": 28,
    "PROGRESS": 29,
    "AVATAR": 30,
    "CHECKBOX": 31,
    "RADIO": 32,
    "SWITCH": 33,
    "DROPDOWN": 34,
    "TABBAR": 35,
    "FORM": 36,
    "PASSWORDINPUT": 37,
    "CHATBUBBLE": 38,
    "SCAFFOLD": 39
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
    action_addresses: dict = field(default_factory=dict)
    action_params: dict = field(default_factory=dict)


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
        self._labels: dict = {}

    def encode(self, lir_nodes: List[LIRNode]) -> EncodedProgram:
        """Encode a list of LIR nodes into a complete binary program."""
        self.pool = ConstantPool()
        self.bytecode = bytearray()
        self.relocations = []
        self._labels = {}
        self._action_addresses = {}
        self._action_addresses_upper = {}

        # Two-pass encoding:
        # Pass 1: Collect action addresses (for CALL resolution)
        # Pass 2: Emit bytecode

        # Pass 1: pre-scan for action declarations to get their addresses
        self._action_params = {}
        fake_offset = 0
        for node in lir_nodes:
            if node.opcode == "ACTION_DECL":
                action_name = node.operands[0]
                args = node.operands[2] if len(node.operands) > 2 else []
                self._action_params[action_name] = args
                # The action body will start after a JMP over it
                # We'll handle this in pass 2
            fake_offset += self._estimate_size(node)

        # Pass 2: emit actual bytecode
        for node in lir_nodes:
            self._encode_node(node)

        # Append HALT
        self._emit(Opcode.HALT, 0)

        # Pass 3: Resolve relocations (JUMPs, CALLs)
        for rel in self.relocations:
            if rel.type in ("CALL", "ACTION"):
                target = self._action_addresses_upper.get(rel.symbol.upper(), self._action_addresses.get(rel.symbol, 0xFFFF))
            else:
                target = self._labels.get(rel.symbol, 0xFFFF)
            
            # Patch the operand (2 bytes) at offset + 1
            self.bytecode[rel.offset + 1] = (target >> 8) & 0xFF
            self.bytecode[rel.offset + 2] = target & 0xFF

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
            relocation_table=self.relocations,
            action_addresses=self._action_addresses,
            action_params=self._action_params
        )

    def _emit(self, opcode: int, operand: int = 0):
        """Emit a single 3-byte instruction."""
        self.bytecode.append(opcode & 0xFF)
        self.bytecode.append((operand >> 8) & 0xFF)
        self.bytecode.append(operand & 0xFF)

    def _encode_node(self, node: LIRNode):
        """Dispatch a single LIR node to the appropriate encoder."""
        opcode = node.opcode
        
        if opcode == "MARK_PAGE_START":
            self._action_addresses["__PAGE_START__"] = len(self.bytecode)
            return

        if opcode == "STATE_INIT":
            self._encode_state_init(node)
        elif opcode == "LOAD_VAR":
            self._encode_load_var(node)
        elif opcode == "STORE_VAR":
            self._encode_store_var(node)
        elif opcode.startswith("BUILD_") and opcode != "BUILD_DICT":
            self._encode_build_widget(node)
        elif opcode.startswith("INIT_") and opcode not in ["INIT_STATE"]:
            node.opcode = "BUILD_" + opcode[5:]
            self._encode_build_widget(node)
        elif opcode == "BUILD_DICT":
            keys = node.operands[0]
            idx = self.pool.add(keys)
            self._emit(Opcode.PUSH_CONST, idx)
            self._emit(Opcode.BUILD_DICT, 0)
        elif opcode == "CREATE_CLOSURE":
            action_name = node.operands[0]
            num_args = node.operands[1]
            action_idx = self.pool.add(action_name)
            self._emit(Opcode.PUSH_CONST, action_idx)
            self._emit(Opcode.CREATE_CLOSURE, num_args)
        elif opcode == "ASYNC_CALL":
            pass # TODO: phase 1.5
        elif opcode == "SETUP_EXCEPT":
            self.relocations.append(Relocation(offset=len(self.bytecode), symbol=node.operands[0], type="JUMP"))
            self._emit(Opcode.SETUP_EXCEPT, 0xFFFF)
        elif opcode == "POP_EXCEPT":
            self._emit(Opcode.POP_EXCEPT, 0)
        elif opcode == "THROW":
            self._emit(Opcode.THROW, 0)
        elif opcode == "RETHROW":
            self._emit(Opcode.RETHROW, 0)
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
        elif opcode == "MARK_BLOCK_START":
            self._emit(Opcode.MARK_BLOCK_START, 0)
        elif opcode == "CREATE_MODEL":
            self._encode_create_model(node)
        elif opcode == "CHECK_AUTH":
            self._emit(Opcode.CHECK_AUTH, 0)
        elif opcode == "REGISTER_ROUTE":
            self._encode_register_route(node)
        elif opcode == "RETURN_VALUE":
            self._encode_return_value(node)
        elif opcode == "NOP":
            pass  # skip no-ops
        elif opcode == "LABEL":
            # Assign current offset to label
            self._labels[node.operands[0]] = len(self.bytecode)
        elif opcode == "JUMP":
            self.relocations.append(Relocation(offset=len(self.bytecode), symbol=node.operands[0], type="JUMP"))
            self._emit(Opcode.JMP, 0xFFFF)
        elif opcode == "JUMP_IF_FALSE":
            self.relocations.append(Relocation(offset=len(self.bytecode), symbol=node.operands[0], type="JUMP_IF_FALSE"))
            self._emit(Opcode.JMP_IF_FALSE, 0xFFFF)
        elif opcode == "GET_ITER":
            self._emit(Opcode.GET_ITER, 0)
        elif opcode == "FOR_ITER":
            # operands: [end_label, iterator_name]
            end_label = node.operands[0]
            iter_name = node.operands[1]
            # operand for FOR_ITER is the name_idx, we jump to end_label if exhausted
            # wait, how to encode jump target and name?
            # Let's push name_idx and then emit FOR_ITER with end_label offset!
            name_idx = self.pool.add(iter_name)
            self._emit(Opcode.PUSH_CONST, name_idx)
            self.relocations.append(Relocation(offset=len(self.bytecode), symbol=end_label, type="FOR_ITER"))
            self._emit(Opcode.FOR_ITER, 0xFFFF)
        elif opcode == "BINARY_OP":
            op = node.operands[0]
            if op == "==": self._emit(Opcode.CMP_EQ, 0)
            elif op == "!=": self._emit(Opcode.CMP_NEQ, 0)
            elif op == "<": self._emit(Opcode.CMP_LT, 0)
            elif op == ">": self._emit(Opcode.CMP_GT, 0)
            elif op == "<=": self._emit(Opcode.CMP_LTE, 0)
            elif op == ">=": self._emit(Opcode.CMP_GTE, 0)
            elif op == "+": self._emit(Opcode.ADD, 0)
            elif op == "-": self._emit(Opcode.SUB, 0)
            elif op == "*": self._emit(Opcode.MUL, 0)
            elif op == "/": self._emit(Opcode.DIV, 0)
            else: self._emit(Opcode.DISPATCH, 0)
        elif opcode == "SET_THEME":
            mode_idx = self.pool.add(node.operands[0])
            self._emit(Opcode.PUSH_CONST, mode_idx)
            self._emit(Opcode.SET_THEME, 0)
        elif opcode == "DECLARE_THEME":
            name_idx = self.pool.add(node.operands[0])
            props_idx = self.pool.add(node.operands[1]) # dict gets serialized automatically in pool.add() if we pass it as a dict or JSON string
            self._emit(Opcode.PUSH_CONST, name_idx)
            self._emit(Opcode.PUSH_CONST, props_idx)
            self._emit(Opcode.DECLARE_THEME, 0)
        elif opcode == "NAVIGATE":
            target = node.operands[0]
            keys = node.operands[1]
            target_idx = self.pool.add(target)
            keys_idx = self.pool.add(keys)
            self._emit(Opcode.PUSH_CONST, target_idx)
            self._emit(Opcode.PUSH_CONST, keys_idx)
            self._emit(Opcode.NAVIGATE, len(keys))
        elif opcode == "BUILD_DICT":
            keys_idx = self.pool.add(node.operands[0])
            self._emit(Opcode.PUSH_CONST, keys_idx)
            self._emit(Opcode.BUILD_DICT, 0)
        elif opcode == "OP_ASYNC_CALL":
            name = node.operands[0]
            num_args = node.operands[1]
            name_idx = self.pool.add(name)
            self._emit(Opcode.PUSH_CONST, name_idx)
            self._emit(Opcode.OP_ASYNC_CALL, num_args)
        elif opcode == "SET_BINDING":
            target_idx = self.pool.add(node.operands[0])
            self._emit(Opcode.PUSH_CONST, target_idx)
            self._emit(Opcode.SET_BINDING, 0)
        elif opcode == "DECLARE_VALIDATION":
            fields_idx = self.pool.add(node.operands[0])
            self._emit(Opcode.PUSH_CONST, fields_idx)
            self._emit(Opcode.DECLARE_VALIDATION, 0)
        elif opcode == "SET_ANIMATION":
            props_idx = self.pool.add(node.operands[0])
            self._emit(Opcode.PUSH_CONST, props_idx)
            self._emit(Opcode.SET_ANIMATION, 0)
        elif opcode == "CREATE_ARRAY":
            # operands[0] is the element count; elements are already on stack
            count = node.operands[0]
            self._emit(Opcode.CREATE_ARRAY, count)
        elif opcode == "GET_LENGTH":
            self._emit(Opcode.GET_LENGTH, 0)
        elif opcode == "LOAD_SUBSCR":
            self._emit(Opcode.LOAD_SUBSCR, 0)
        elif opcode == "STORE_SUBSCR":
            self._emit(Opcode.STORE_SUBSCR, 0)
        elif opcode == "DECLARE_LIFECYCLE":
            hook = node.operands[0]
            body_lir = node.operands[1]
            hook_idx = self.pool.add(hook)
            self._emit(Opcode.PUSH_CONST, hook_idx)
            # Encode body as an inline block for lifecycle
            # we need a jump around it
            import uuid
            end_label = f"lifecycle_end_{uuid.uuid4().hex[:8]}"
            self.relocations.append(Relocation(offset=len(self.bytecode), symbol=end_label, type="JUMP"))
            self._emit(Opcode.JMP, 0xFFFF)
            
            start_offset = len(self.bytecode)
            for stmt in body_lir:
                self._encode_node(stmt)
            self._emit(Opcode.RET, 0)
            
            self._labels[end_label] = len(self.bytecode)
            
            # Now we need to pass the start offset to DECLARE_LIFECYCLE
            # So DECLARE_LIFECYCLE operand is the action pointer (start_offset)
            # Actually, to make it simpler, we just emit DECLARE_LIFECYCLE with start_offset!
            self._emit(Opcode.DECLARE_LIFECYCLE, start_offset)
            
        else:
            # Unknown LIR opcode — emit as DISPATCH for extensibility
            self._emit(Opcode.DISPATCH, 0)

    def _encode_state_init(self, node: LIRNode):
        """STATE_INIT [name]
        Value is already on stack!
        → INIT_STATE name_idx
        """
        name = node.operands[0]
        name_idx = self.pool.add(name)
        self._emit(Opcode.INIT_STATE, name_idx)

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
            # Removing text to value mapping as it duplicates $STACK markers and causes underflow
            idx = self.pool.add(props)
            self._emit(Opcode.PUSH_CONST, idx)
        elif isinstance(props, str):
            if props == "__DYNAMIC__":
                pass # Skip pushing, value is already on stack
            else:
                text_idx = self.pool.add(props)
                self._emit(Opcode.PUSH_CONST, text_idx)
        else:
            empty_idx = self.pool.add("")
            self._emit(Opcode.PUSH_CONST, empty_idx)

        if widget_type_id == 0:
            # Custom Component!
            # The props dict is on the stack (if dict)
            # Emit CALL_COMPONENT instead of BUILD_WIDGET
            if widget_type_str in self._action_addresses_upper:
                target = self._action_addresses_upper[widget_type_str]
                self._emit(Opcode.CALL_COMPONENT, target)
            else:
                self.relocations.append(Relocation(
                    offset=len(self.bytecode),
                    symbol=widget_type_str,
                    type="CALL" # We can just keep type as CALL for relocation patching
                ))
                self._emit(Opcode.CALL_COMPONENT, 0xFFFF)
        else:
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
        action_name = node.operands[0]
        
        # Jump over the action body so it doesn't execute inline
        self._emit(Opcode.JMP, 0xFFFF)
        jmp_addr = len(self.bytecode) - 2 # The operand offset

        self._action_addresses[action_name] = len(self.bytecode)
        self._action_addresses_upper[action_name.upper()] = len(self.bytecode)

        if len(node.operands) > 2:
            args = node.operands[2]
            for arg in reversed(args):
                arg_idx = self.pool.add(arg)
                self._emit(Opcode.STORE_STATE, arg_idx)

        # Encode body statements
        if len(node.operands) > 1:
            body_nodes = node.operands[1]
            if isinstance(body_nodes, list):
                for sub_node in body_nodes:
                    if isinstance(sub_node, LIRNode):
                        self._encode_node(sub_node)

        # Return from action
        self._emit(Opcode.RET, 0)
        
        # Patch the JMP operand
        end_addr = len(self.bytecode)
        self.bytecode[jmp_addr] = (end_addr >> 8) & 0xFF
        self.bytecode[jmp_addr + 1] = end_addr & 0xFF

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
        elif opcode == "REGISTER_ROUTE":
            return 6  # PUSH_CONST + REGISTER_ROUTE (methods counted recursively)
        else:
            return 3  # single instruction

    def _encode_create_model(self, node: LIRNode):
        model_name = node.operands[0]
        fields = node.operands[1]
        decorators = node.operands[2] if len(node.operands) > 2 else []
        
        name_idx = self.pool.add(model_name)
        payload = {"fields": fields, "decorators": decorators}
        fields_idx = self.pool.add(payload)
        
        self._emit(Opcode.PUSH_CONST, name_idx)
        self._emit(Opcode.CREATE_MODEL, fields_idx)

    def _encode_register_route(self, node: LIRNode):
        path = node.operands[0]
        methods = node.operands[1]
        
        methods_meta = []
        for method_data in methods:
            method = method_data["method"]
            body_nodes = method_data["body"]
            
            # Jump over the method body
            self._emit(Opcode.JMP, 0xFFFF)
            jmp_addr = len(self.bytecode) - 2
            
            start_addr = len(self.bytecode)
            for sub_node in body_nodes:
                self._encode_node(sub_node)
            
            # Implicit return at the end of the route method
            self._emit(Opcode.RET, 0)
            
            # Patch jump
            end_addr = len(self.bytecode)
            self.bytecode[jmp_addr] = (end_addr >> 8) & 0xFF
            self.bytecode[jmp_addr + 1] = end_addr & 0xFF
            
            methods_meta.append({"method": method, "target_address": start_addr})
            
        # Emit REGISTER_ROUTE
        path_idx = self.pool.add(path)
        meta_idx = self.pool.add(methods_meta)
        
        self._emit(Opcode.PUSH_CONST, path_idx)
        self._emit(Opcode.REGISTER_ROUTE, meta_idx)

    def _encode_return_value(self, node: LIRNode):
        self._emit(Opcode.RETURN_VALUE, 0)
