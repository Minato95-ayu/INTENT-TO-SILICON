# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

"""
compiler.ir.linearizer — Out-of-SSA lowering + block serialization
==================================================================

The final compiler pass before bytecode emission.  Takes an optimized
SSA-form CFG and produces a flat list of stack-based MIR instructions
that the legacy AAYU VM can execute directly.

Three-stage pipeline
--------------------
1. **Out-of-SSA (PHI elimination)** — replaces PHI nodes with explicit
   COPY instructions at the end of each predecessor block.
2. **Block linearization** — serializes the CFG into a flat instruction
   list with LABEL markers.
3. **3AC → stack lowering** — translates three-address-code virtual
   register operations into push/pop stack-machine instructions.

Value → VM mapping
------------------
Each SSA ``Value`` is mapped to a synthetic VM local variable named
``"%v{id}"`` (e.g. ``%v3``).  These are not user-visible variable names;
they exist solely to bridge the register-based SSA world with the
stack-based VM.

See Also
--------
compiler.ir.optimizer : Optimization pass that runs before this.
compiler.bytecode.encoder : Bytecode emission that runs after this.
"""

from typing import Any, List

from compiler.ir.mir_cfg import CFG, BasicBlock, Branch, Jump, Return
from compiler.ir.mir import MIRInstruction, Value


# Functions that the VM dispatches as built-in async calls rather than
# user-defined actions.  Shared between Linearizer and legacy pipeline.
BUILTIN_FUNCTIONS = frozenset({
    "print", "len", "type", "float", "int",
})


class Linearizer:
    """Converts an SSA-form CFG into a flat list of stack-machine instructions.

    Usage::

        mir_list = Linearizer(cfg).lower()

    Parameters
    ----------
    cfg : CFG
        The SSA-form CFG to lower (mutated by ``out_of_ssa``).
    """

    def __init__(self, cfg: CFG):
        self.cfg = cfg
        self._mir_list: List[MIRInstruction] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def lower(self) -> List[MIRInstruction]:
        """Run the full lowering pipeline and return the flat instruction list.

        Returns
        -------
        list[MIRInstruction]
            A linear sequence of stack-machine instructions with LABEL
            targets, ready for LIR conversion and bytecode emission.
        """
        self._out_of_ssa()
        self._mir_list = []
        self._linearize_blocks()
        return self._mir_list

    # ------------------------------------------------------------------
    # Stage 1: Out-of-SSA (PHI elimination)
    # ------------------------------------------------------------------

    def _out_of_ssa(self) -> None:
        """Eliminate PHI nodes by inserting COPY instructions.

        For each PHI ``%x = PHI({B1: %y, B2: %z})`` in block B:
        - At the end of predecessor B1, insert ``COPY %y → %x``.
        - At the end of predecessor B2, insert ``COPY %z → %x``.
        - Remove the PHI from block B.

        Note: Each COPY gets its own fresh result Value to maintain
        the single-definition property during lowering.  The lowered
        stack code writes to the same VM local (``%v{original_phi_id}``),
        so the semantics are preserved.
        """
        for block in self.cfg.blocks:
            phi_instructions = [inst for inst in block.instructions
                                if inst.opcode == "PHI"]
            block.instructions = [inst for inst in block.instructions
                                  if inst.opcode != "PHI"]

            for phi in phi_instructions:
                phi_dict = phi.operands[0]
                original_result = phi.result

                for pred, val in phi_dict.items():
                    # Create a COPY that writes to a fresh Value, but
                    # the Linearizer will lower it to SET_STATE using
                    # the *original* PHI result's id — so all paths
                    # converge on the same VM local.
                    copy_inst = MIRInstruction(
                        opcode="COPY", operands=[val])
                    copy_result = Value(
                        id=original_result.id,
                        name=f"phi_copy_{original_result.id}",
                    )
                    copy_inst.result = copy_result
                    pred.instructions.append(copy_inst)

    # ------------------------------------------------------------------
    # Stage 2 + 3: Linearize blocks and lower to stack code
    # ------------------------------------------------------------------

    def _linearize_blocks(self) -> None:
        """Serialize all CFG blocks into a flat instruction list using DFS."""
        if not self.cfg.blocks:
            return

        visited = set()
        ordered_blocks = []

        def dfs(block):
            if block.id in visited:
                return
            visited.add(block.id)
            ordered_blocks.append(block)

            # Traverse children (true branch first for better fall-through)
            term = block.terminator
            from compiler.ir.mir_cfg import Branch, Jump
            if isinstance(term, Branch):
                dfs(term.true_target)
                dfs(term.false_target)
            elif isinstance(term, Jump):
                dfs(term.target)

        # Start from the entry block (assuming it's the first in the list)
        # Fallback for unconnected blocks just in case
        dfs(self.cfg.blocks[0])
        for block in self.cfg.blocks:
            if block.id not in visited:
                dfs(block)

        for block in ordered_blocks:
            self._emit("LABEL", [block.id])
            self._lower_block_instructions(block)
            self._lower_terminator(block)

    def _lower_block_instructions(self, block: BasicBlock) -> None:
        """Lower all instructions in a single block to stack-machine ops."""
        for inst in block.instructions:
            if inst.opcode == "CONST":
                self._emit("PUSH_CONST", [inst.operands[0]])
                self._pop_to(inst.result)

            elif inst.opcode == "COPY":
                self._push_value(inst.operands[0])
                self._pop_to(inst.result)

            elif inst.opcode.startswith("BINARY_"):
                self._push_value(inst.operands[0])
                self._push_value(inst.operands[1])
                op = inst.opcode[7:]  # Strip "BINARY_" prefix.
                self._emit("BINARY_OP", [op])
                self._pop_to(inst.result)

            elif inst.opcode.startswith("UNARY_"):
                self._push_value(inst.operands[0])
                op = inst.opcode[6:]  # Strip "UNARY_" prefix.
                self._emit("UNARY_OP", [op])
                self._pop_to(inst.result)

            elif inst.opcode == "CALL":
                self._lower_call(inst)

            elif inst.opcode == "PRINT":
                self._push_value(inst.operands[0])
                self._emit("OP_ASYNC_CALL", ["print", 1])
                self._emit("POP", [])

            elif inst.opcode == "HAS_NEXT":
                self._push_value(inst.operands[0])
                self._emit("HAS_NEXT", [])
                self._pop_to(inst.result)

            elif inst.opcode == "NEXT_ITEM":
                self._push_value(inst.operands[0])
                self._emit("NEXT_ITEM", [])
                self._pop_to(inst.result)

            elif inst.opcode == "BUILD_LIST":
                for elem in inst.operands:
                    self._push_value(elem)
                self._emit("CREATE_ARRAY", [len(inst.operands)])
                self._pop_to(inst.result)

            elif inst.opcode == "ACTION_DECL":
                self._lower_action_decl(inst)

            elif inst.opcode == "POP_EXCEPTION":
                # Exception is already on the VM stack from _throw_exception
                self._pop_to(inst.result)

            elif inst.opcode == "THROW":
                self._push_value(inst.operands[0])
                self._emit("THROW", [])
                
            elif inst.opcode == "RETHROW":
                self._emit("RETHROW", [])

            else:
                # Pass through for advanced structures not fully lowered
                # yet (e.g. UI widgets, models).  Filter out opcodes that
                # should have been eliminated by previous passes.
                if inst.opcode not in ("LOAD_VAR", "SET_STATE",
                                       "STORE_VAR", "PHI"):
                    self._mir_list.append(inst)

    def _lower_terminator(self, block: BasicBlock) -> None:
        """Lower a block's terminator to stack-machine jump instructions."""
        term = block.terminator

        if isinstance(term, Jump):
            self._emit("JUMP", [term.target.id])

        elif isinstance(term, Branch):
            self._push_value(term.condition)
            self._emit("JUMP_IF_FALSE", [term.false_target.id])
            self._emit("JUMP", [term.true_target.id])

        elif isinstance(term, Return):
            if term.value is not None:
                self._push_value(term.value)
                self._emit("RETURN_VALUE", [])
            else:
                self._emit("RET", [])

    # ------------------------------------------------------------------
    # Lowering helpers for specific opcodes
    # ------------------------------------------------------------------

    def _lower_call(self, inst: MIRInstruction) -> None:
        """Lower a CALL instruction to the appropriate VM call opcode.

        - Built-in functions (print, len, etc.) → ``OP_ASYNC_CALL``
        - Dotted names (e.g. ``"list.append"``) → ``OP_ASYNC_CALL``
        - User-defined actions → ``CALL_ACTION``
        """
        name = inst.operands[0]
        args = inst.operands[1:]

        for arg in args:
            self._push_value(arg)

        if "." in name or "::" in name or name in BUILTIN_FUNCTIONS:
            self._emit("OP_ASYNC_CALL", [name, len(args)])
            if inst.result is None:
                self._emit("POP", [])
            else:
                self._pop_to(inst.result)
        else:
            return_count = 1 if inst.result is not None else 0
            self._emit("CALL_ACTION", [name, len(args), return_count])
            self._pop_to(inst.result)

    def _lower_action_decl(self, inst: MIRInstruction) -> None:
        """Lower an ACTION_DECL by recursively linearizing the nested CFG."""
        name = inst.operands[0]
        action_cfg = inst.operands[1]
        args = inst.operands[2]

        # Recursively lower the action's own CFG.
        body_mir = Linearizer(action_cfg).lower()
        self._mir_list.append(
            MIRInstruction("ACTION_DECL", [name, body_mir, args]))

    # ------------------------------------------------------------------
    # Stack manipulation primitives
    # ------------------------------------------------------------------

    def _push_value(self, val: Any) -> None:
        """Push a value onto the VM stack.

        - ``Value`` objects → ``LOAD_VAR "%v{id}"``
        - Literals (int, str, bool, None) → ``PUSH_CONST literal``
        """
        if isinstance(val, Value):
            self._emit("LOAD_VAR", [f"%v{val.id}"])
        else:
            self._emit("PUSH_CONST", [val])

    def _pop_to(self, val: Value) -> None:
        """Pop the top-of-stack into a VM local variable.

        Emits ``SET_STATE "%v{id}"`` if *val* is not None.
        """
        if val is not None:
            self._emit("SET_STATE", [f"%v{val.id}"])

    def _emit(self, opcode: str, operands: List[Any]) -> None:
        """Append a raw MIR instruction to the output list."""
        self._mir_list.append(MIRInstruction(opcode, operands))
