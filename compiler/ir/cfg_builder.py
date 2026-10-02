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
compiler.ir.cfg_builder — HIR → CFG lowering pass
==================================================

Translates the High-level IR (HIR) tree into a Control-Flow Graph (CFG)
of three-address-code (3AC) MIR instructions.

Supported HIR nodes
-------------------
HIRLoadConst, HIRLoadVar, HIRBinaryOp, HIRStateDecl, HIRAssignment,
HIRIf, HIRFor, HIRReturn, HIRPrint, HIRActionCall, HIRActionDecl.

Design notes
------------
- Each top-level ``build()`` call produces **one** CFG per action / module.
- Nested ``HIRActionDecl`` nodes get their **own** CFG (stored as an
  operand of an ``ACTION_DECL`` instruction in the parent CFG).
- Boolean keywords ``true`` / ``false`` / ``null`` are folded to ``CONST``
  instructions here because the semantic analyzer registers them as
  identifiers (``SemanticIdentifierNode``), not as literal nodes.
  This is a pragmatic workaround; ideally the semantic layer should emit
  ``HIRLoadConst(True)`` directly.

See Also
--------
compiler.ir.mir_cfg : CFG / BasicBlock / Terminator definitions.
compiler.ir.ssa     : SSA construction pass that runs after this.
"""

from typing import List, Optional, Any

from compiler.ir.hir import (
    HIRNode, HIRStateDecl, HIRWidget, HIRAssignment,
    HIRActionDecl, HIRActionCall, HIRLoadVar, HIRPrint, HIRImport,
    HIRIf, HIRFor, HIRBinaryOp, HIRLoadConst,
    HIRModel, HIRModelField, HIRModelAttribute, HIRRoute, HIRMethod,
    HIRReturn, HIRArrayNode, HIRSubscript,
)
from compiler.ir.mir import MIRInstruction, Value
from compiler.ir.mir_cfg import CFG, BasicBlock, Jump, Branch, Return


# Names that the semantic analyzer registers as global boolean / null
# constants.  We fold them to ``CONST`` instructions so the SSA optimizer
# can propagate and eliminate branches on them.
_BUILTIN_CONSTANTS = {
    "true":  True,
    "false": False,
    "null":  None,
}


class CFGBuilder:
    """Lowers a list of HIR nodes into a single CFG of 3AC instructions.

    Usage::

        builder = CFGBuilder()
        cfg = builder.build("main", hir_nodes)

    The returned ``CFG`` has:
    - One ``entry_block`` named ``entry_{action_name}``.
    - Additional blocks for branches, loops, and merge points.
    - Each block's instruction list uses ``Value`` objects for explicit
      def-use relationships (three-address code).
    """

    def __init__(self):
        self.current_cfg: Optional[CFG] = None
        self.current_block: Optional[BasicBlock] = None
        self.value_counter: int = 0

    # ------------------------------------------------------------------
    # Value factory
    # ------------------------------------------------------------------

    def _next_value(self) -> Value:
        """Allocate a fresh virtual register with a unique id."""
        self.value_counter += 1
        return Value(id=self.value_counter)

    # ------------------------------------------------------------------
    # Instruction emitter
    # ------------------------------------------------------------------

    def _emit(self, opcode: str, operands: List[Any],
              has_result: bool = True) -> Optional[Value]:
        """Append a MIR instruction to the current block.

        Parameters
        ----------
        opcode : str
            The instruction opcode (e.g. ``"CONST"``, ``"BINARY_+"``).
        operands : list
            Instruction operands (Values, literals, strings).
        has_result : bool
            If True, a fresh ``Value`` is allocated and linked as the
            instruction's ``result``.

        Returns
        -------
        Value | None
            The result Value, or None if ``has_result`` is False.

        Notes
        -----
        If the current block is ``None`` or already terminated (e.g. code
        after a ``return``), the instruction is silently discarded — this
        handles unreachable code gracefully.
        """
        if self.current_block is None or self.current_block.is_terminated():
            # Unreachable code — still allocate a Value so that any
            # downstream references don't crash, but don't emit.
            return self._next_value() if has_result else None

        inst = MIRInstruction(opcode, operands)
        if has_result:
            val = self._next_value()
            val.defining_inst = inst
            inst.result = val
            self.current_block.instructions.append(inst)
            return val
        else:
            self.current_block.instructions.append(inst)
            return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self, action_name: str, hir_nodes: List[HIRNode]) -> CFG:
        """Lower a list of HIR nodes into a CFG.

        Parameters
        ----------
        action_name : str
            Name for the resulting CFG (used in block id prefixes).
        hir_nodes : list[HIRNode]
            The HIR statements to lower.

        Returns
        -------
        CFG
            The completed control-flow graph.
        """
        self.current_cfg = CFG(action_name)
        self.current_block = self.current_cfg.entry_block
        self.value_counter = 0

        for node in hir_nodes:
            self._lower_hir(node)

        # Ensure every block has a terminator (implicit void return).
        if self.current_block and not self.current_block.is_terminated():
            self.current_block.set_terminator(Return(None))

        return self.current_cfg

    # ------------------------------------------------------------------
    # HIR → CFG dispatch
    # ------------------------------------------------------------------

    def _lower_hir(self, hir: HIRNode) -> Optional[Value]:
        """Recursively lower a single HIR node into the current CFG block.

        This is the central dispatch method.  Each HIR node type has its
        own lowering logic:

        - **Expressions** (LoadConst, LoadVar, BinaryOp) produce a result
          ``Value`` and append instructions to the current block.
        - **Statements** (Assignment, If, For, Return) may create new
          blocks and wire terminators.
        - **Declarations** (ActionDecl) build a nested CFG.

        Returns
        -------
        Value | None
            The result Value for expressions, ``None`` for statements.

        Raises
        ------
        NotImplementedError
            If the HIR node type is not handled.  This ensures that adding
            a new HIR node without updating the CFG builder fails loudly
            rather than silently emitting garbage instructions.
        """
        # Guard: skip if we're in unreachable code (after a return, etc.)
        if self.current_block is None or self.current_block.is_terminated():
            return None

        # -- Declarations ---------------------------------------------------

        if isinstance(hir, HIRActionDecl):
            return self._lower_action_decl(hir)

        # -- Control flow ---------------------------------------------------

        elif isinstance(hir, HIRIf):
            return self._lower_if(hir)

        elif isinstance(hir, HIRFor):
            return self._lower_for(hir)

        elif isinstance(hir, HIRReturn):
            return self._lower_return(hir)

        # -- Expressions ----------------------------------------------------

        elif isinstance(hir, HIRLoadConst):
            return self._emit("CONST", [hir.value])

        elif isinstance(hir, HIRAssignment) or isinstance(hir, HIRStateDecl):
            val = self._lower_hir(hir.value)
            target = (hir.target if isinstance(hir, HIRAssignment)
                      else getattr(hir, 'name', ''))
            self._emit("STORE_VAR", [target, val], has_result=False)
            return None

        elif isinstance(hir, HIRLoadVar):
            # Fold built-in constants (true / false / null) to CONST.
            # See module docstring for rationale.
            if hir.name in _BUILTIN_CONSTANTS:
                return self._emit("CONST", [_BUILTIN_CONSTANTS[hir.name]])
            return self._emit("LOAD_VAR", [hir.name])

        elif isinstance(hir, HIRBinaryOp):
            left_val = self._lower_hir(hir.left)
            right_val = self._lower_hir(hir.right)
            return self._emit(f"BINARY_{hir.op}", [left_val, right_val])

        elif isinstance(hir, HIRPrint):
            val = self._lower_hir(hir.value)
            self._emit("PRINT", [val], has_result=False)
            return None

        elif isinstance(hir, HIRArrayNode):
            # Lower each element, then emit a BUILD_LIST instruction.
            element_vals = [self._lower_hir(elem)
                            for elem in hir.elements]
            return self._emit("BUILD_LIST", element_vals)

        elif isinstance(hir, HIRActionCall):
            arg_vals = [self._lower_hir(arg)
                        for arg in getattr(hir, 'args', [])]
            return self._emit("CALL", [hir.name] + arg_vals)

        # -- Exceptions -----------------------------------------------------
        elif type(hir).__name__ == "HIRTry":
            return self._lower_try(hir)

        elif type(hir).__name__ == "HIRThrow":
            val = self._lower_hir(hir.value)
            self._emit("THROW", [val], has_result=False)
            return None

        elif type(hir).__name__ == "HIRRethrow":
            self._emit("RETHROW", [], has_result=False)
            return None

        # -- Unknown --------------------------------------------------------

        else:
            raise NotImplementedError(
                f"CFG lowering not implemented for HIR node type "
                f"'{type(hir).__name__}'.  Add a handler in "
                f"CFGBuilder._lower_hir() before using this construct."
            )

    # ------------------------------------------------------------------
    # Lowering helpers — one per compound HIR node
    # ------------------------------------------------------------------

    def _lower_action_decl(self, hir: HIRActionDecl) -> Optional[Value]:
        """Lower an action declaration into a nested CFG.

        The nested CFG is stored as an operand of an ``ACTION_DECL``
        instruction in the **parent** CFG.  The Linearizer will
        recursively lower it later.

        Important: ``value_counter`` is saved and restored so that the
        parent and child scopes don't collide on Value ids.
        """
        # Save parent context
        saved_cfg = self.current_cfg
        saved_block = self.current_block
        saved_counter = self.value_counter

        # Build child CFG
        action_cfg = CFG(hir.name)
        self.current_cfg = action_cfg
        self.current_block = action_cfg.entry_block
        self.value_counter = 0  # fresh scope

        for stmt in hir.body:
            self._lower_hir(stmt)

        # Ensure the child CFG has a terminator
        if self.current_block and not self.current_block.is_terminated():
            self.current_block.set_terminator(Return(None))

        # Restore parent context
        self.current_cfg = saved_cfg
        self.current_block = saved_block
        self.value_counter = saved_counter

        return self._emit("ACTION_DECL", [hir.name, action_cfg, hir.args])

    def _lower_if(self, hir: HIRIf) -> None:
        """Lower an if/else into a diamond-shaped CFG subgraph.

        ::

            [entry]
              │
              BR cond
             / \\
          [then] [else]
             \\ /
            [merge]
        """
        cond_val = self._lower_hir(hir.condition)
        if not isinstance(cond_val, Value):
            cond_val = self._next_value()

        then_block = self.current_cfg.add_block("then")
        else_block = self.current_cfg.add_block("else")
        merge_block = self.current_cfg.add_block("endif")

        self.current_block.set_terminator(
            Branch(cond_val, then_block, else_block))

        # Then branch
        self.current_block = then_block
        for stmt in hir.then_branch:
            self._lower_hir(stmt)
        if not self.current_block.is_terminated():
            self.current_block.set_terminator(Jump(merge_block))

        # Else branch
        self.current_block = else_block
        if getattr(hir, 'else_branch', None):
            for stmt in hir.else_branch:
                self._lower_hir(stmt)
        if not self.current_block.is_terminated():
            self.current_block.set_terminator(Jump(merge_block))

        self.current_block = merge_block
        return None

    def _lower_for(self, hir: HIRFor) -> None:
        """Lower a for-in loop into a header / body / exit structure.

        ::

            [entry]
              │ JUMP
            [header]  ←──┐
              │ BR        │
             / \\         │
          [body]  [exit]  │
              │           │
              └───────────┘
        """
        iter_val = self._lower_hir(hir.iterable)

        loop_header = self.current_cfg.add_block("loop_header")
        loop_body = self.current_cfg.add_block("loop_body")
        loop_exit = self.current_cfg.add_block("loop_exit")

        self.current_block.set_terminator(Jump(loop_header))

        # Header: check iteration condition
        self.current_block = loop_header
        cond_val = self._emit("HAS_NEXT", [iter_val])
        self.current_block.set_terminator(
            Branch(cond_val, loop_body, loop_exit))

        # Body: extract item, execute statements, back-edge to header
        self.current_block = loop_body
        item_val = self._emit("NEXT_ITEM", [iter_val])
        self._emit("STORE_VAR", [hir.iterator, item_val], has_result=False)

        for stmt in hir.body:
            self._lower_hir(stmt)
        if not self.current_block.is_terminated():
            self.current_block.set_terminator(Jump(loop_header))

        self.current_block = loop_exit
        return None

    def _lower_return(self, hir: HIRReturn) -> None:
        """Lower a return statement.

        After setting the ``Return`` terminator, the current block is
        effectively sealed — any subsequent instructions are unreachable
        and will be skipped by the ``is_terminated()`` guard in ``_emit``.
        """
        ret_val = None
        if hir.value:
            ret_val = self._lower_hir(hir.value)
        self.current_block.set_terminator(Return(ret_val))
        return None

    def _lower_try(self, hir: Any) -> None:
        """Lower try/catch/finally block."""
        import uuid
        uid = uuid.uuid4().hex[:8]
        catch_block = self.current_cfg.add_block(f"catch_{uid}")
        finally_block = self.current_cfg.add_block(f"finally_{uid}")
        
        error_target = catch_block if hir.catch_block else finally_block
        
        self._emit("SETUP_EXCEPT", [error_target.id], has_result=False)
        
        if error_target not in self.current_block.successors:
            self.current_block.successors.append(error_target)
        if self.current_block not in error_target.predecessors:
            error_target.predecessors.append(self.current_block)
        
        for stmt in hir.try_block:
            self._lower_hir(stmt)
            
        if not self.current_block.is_terminated():
            self._emit("POP_EXCEPT", [], has_result=False)
            self.current_block.set_terminator(Jump(finally_block))
            
        if hir.catch_block:
            self.current_block = catch_block
            if hir.catch_var:
                exc_val = self._emit("POP_EXCEPTION", [])
                self._emit("STORE_VAR", [hir.catch_var, exc_val], has_result=False)
            else:
                self._emit("POP_EXCEPTION", [])
                
            for stmt in hir.catch_block:
                self._lower_hir(stmt)
                
            if not self.current_block.is_terminated():
                self.current_block.set_terminator(Jump(finally_block))
                
        self.current_block = finally_block
        for stmt in hir.finally_block:
            self._lower_hir(stmt)
        
        return None
