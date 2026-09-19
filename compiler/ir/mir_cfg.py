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
compiler.ir.mir_cfg — Control Flow Graph (CFG) infrastructure
=============================================================

Defines the core graph structures used by every pass from R4.1 onward:

    BasicBlock   — a straight-line sequence of MIR instructions ending in
                   exactly one Terminator.
    Terminator   — Jump | Branch | Return.
    CFG          — the complete control-flow graph for a single function /
                   action.

Threading model
---------------
``set_terminator()`` automatically wires up predecessor / successor edges.
Each block may be terminated **at most once**; a second attempt raises
``InternalCompilerError`` so that CFG-construction bugs surface immediately
instead of being silently swallowed.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from compiler.ir.mir import MIRInstruction, Value


# ---------------------------------------------------------------------------
# Internal error — raised when a compiler invariant is violated.
# ---------------------------------------------------------------------------

class InternalCompilerError(Exception):
    """Raised when an internal compiler invariant is violated.

    This is *not* a user-facing error — it indicates a bug in the compiler
    itself.  If you see this in production, file a bug report.
    """
    pass


# ---------------------------------------------------------------------------
# Terminators — every BasicBlock ends with exactly one of these.
# ---------------------------------------------------------------------------

@dataclass
class Terminator:
    """Base class for block terminators.  Not instantiated directly."""
    pass


@dataclass
class Jump(Terminator):
    """Unconditional jump to *target* block."""
    target: 'BasicBlock'

    def __repr__(self) -> str:
        return f"Jump → {self.target.id}"


@dataclass
class Branch(Terminator):
    """Conditional branch.

    Evaluates *condition* (a ``Value`` or literal) and transfers control to
    *true_target* if truthy, *false_target* otherwise.
    """
    condition: Any  # Value or literal (after constant propagation)
    true_target: 'BasicBlock'
    false_target: 'BasicBlock'

    def __repr__(self) -> str:
        return (f"Branch({self.condition}) "
                f"→ T:{self.true_target.id} / F:{self.false_target.id}")


@dataclass
class Return(Terminator):
    """Return from the current function / action.

    *value* is ``None`` for void returns.
    """
    value: Optional[Any] = None  # Value or literal (after const-prop)

    def __repr__(self) -> str:
        return f"Return({self.value})"


# ---------------------------------------------------------------------------
# BasicBlock
# ---------------------------------------------------------------------------

@dataclass
class BasicBlock:
    """A linear sequence of MIR instructions ending in exactly one terminator.

    Identity (``__eq__`` / ``__hash__``) is based solely on the string
    ``id`` to avoid infinite recursion when blocks form cycles (back-edges).
    """

    id: str
    instructions: List[MIRInstruction] = field(default_factory=list)
    terminator: Optional[Terminator] = None
    predecessors: List['BasicBlock'] = field(default_factory=list)
    successors: List['BasicBlock'] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Identity by id — required for hashability in dominator sets / dicts.
    # ------------------------------------------------------------------

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BasicBlock):
            return False
        return self.id == other.id

    def __repr__(self) -> str:
        return f"BB({self.id}, {len(self.instructions)} insts)"

    # ------------------------------------------------------------------
    # Terminator wiring
    # ------------------------------------------------------------------

    def set_terminator(self, term: Terminator) -> None:
        """Set this block's terminator and automatically wire predecessor /
        successor edges.

        Raises
        ------
        InternalCompilerError
            If the block has already been terminated.  This catches CFG
            construction bugs early (e.g. forgetting an ``is_terminated()``
            guard before emitting a second branch).
        """
        if self.terminator is not None:
            raise InternalCompilerError(
                f"Block '{self.id}' is already terminated by {self.terminator!r}. "
                f"Attempted to set a second terminator: {term!r}. "
                f"This is a compiler bug — check the CFG builder logic."
            )

        self.terminator = term

        # Wire edges, guarding against duplicates.
        if isinstance(term, Jump):
            if term.target not in self.successors:
                self.successors.append(term.target)
            if self not in term.target.predecessors:
                term.target.predecessors.append(self)

        elif isinstance(term, Branch):
            for target in (term.true_target, term.false_target):
                if target not in self.successors:
                    self.successors.append(target)
                if self not in target.predecessors:
                    target.predecessors.append(self)

        # Return has no successors — nothing to wire.

    def is_terminated(self) -> bool:
        """Return True if this block already has a terminator."""
        return self.terminator is not None


# ---------------------------------------------------------------------------
# CFG — one per function / action
# ---------------------------------------------------------------------------

@dataclass
class CFG:
    """Control-flow graph for a single function / action.

    On construction, an *entry block* named ``entry_{name}`` is created
    automatically and added to ``self.blocks``.

    Attributes
    ----------
    name : str
        The function / action name (used for labels and debug output).
    entry_block : BasicBlock
        The first block executed when the function is entered.
    blocks : list[BasicBlock]
        All blocks in the CFG, in insertion order.
    """

    name: str
    entry_block: BasicBlock = field(init=False)
    blocks: List[BasicBlock] = field(default_factory=list)

    def __init__(self, name: str):
        self.name = name
        self.entry_block = BasicBlock(f"entry_{name}")
        self.blocks = [self.entry_block]

    def add_block(self, prefix: str = "block") -> BasicBlock:
        """Create a new block with a unique id and append it to the CFG.

        Parameters
        ----------
        prefix : str
            Human-readable prefix for the block id (e.g. ``"then"``,
            ``"loop_header"``).  A numeric suffix is appended to ensure
            uniqueness within this CFG.

        Returns
        -------
        BasicBlock
            The newly created block.
        """
        block_id = f"{prefix}_{len(self.blocks)}"
        block = BasicBlock(block_id)
        self.blocks.append(block)
        return block

    # ------------------------------------------------------------------
    # Visualization
    # ------------------------------------------------------------------

    def to_dot(self) -> str:
        """Export the CFG to Graphviz DOT format for visualization.

        Usage::

            with open("cfg.dot", "w") as f:
                f.write(cfg.to_dot())
            # Then: dot -Tpng cfg.dot -o cfg.png
        """
        lines = [f'digraph {self.name} {{', '  node [shape=box];']

        for block in self.blocks:
            # Build instruction listing
            instr_lines = []
            for inst in block.instructions:
                ops = ", ".join(map(str, inst.operands))
                res = f"{inst.result} = " if inst.result else ""
                instr_lines.append(f"{res}{inst.opcode} {ops}")

            instr_str = "\\n".join(instr_lines)

            # Build terminator string
            term = block.terminator
            if isinstance(term, Jump):
                term_str = f"JUMP {term.target.id}"
            elif isinstance(term, Branch):
                term_str = (f"BR {term.condition}, "
                            f"{term.true_target.id}, {term.false_target.id}")
            elif isinstance(term, Return):
                term_str = f"RET {term.value}"
            else:
                term_str = "<?>"

            label = f"{block.id}\\n---\\n{instr_str}\\n---\\n{term_str}"
            label = label.replace("\"", "\\\"")
            lines.append(f'  {block.id} [label="{label}"];')

            # Edges
            for succ in block.successors:
                if isinstance(term, Branch):
                    edge_label = ("true" if succ == term.true_target
                                  else "false")
                    lines.append(
                        f'  {block.id} -> {succ.id} [label="{edge_label}"];')
                else:
                    lines.append(f'  {block.id} -> {succ.id};')

        lines.append('}')
        return "\n".join(lines)
