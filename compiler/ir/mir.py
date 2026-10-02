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
compiler.ir.mir — Mid-level Intermediate Representation (MIR)
=============================================================

This module defines the canonical instruction and value types used by AAYU's
optimizing compiler pipeline:

    HIR  →  CFG (mir_cfg)  →  3AC Instructions (this module)  →  SSA  →  Optimizer  →  Linearizer  →  Bytecode

Key types
---------
- **Value**          : A virtual register / SSA value. Identity is determined
                       solely by its numeric ``id``; two Values with the same
                       id are considered the same register regardless of other
                       fields.
- **MIRInstruction** : A single three-address-code operation with an opcode,
                       a list of operands, and an optional result Value.

Design notes
------------
- ``Value.__eq__`` and ``Value.__hash__`` are overridden to compare by ``id``
  only.  This is critical for correct behaviour in sets, dicts, and the
  dominator / SSA passes that use Values as keys.
- ``MIRInstruction.result`` links back to the Value it defines (def-use chain).
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional


# ---------------------------------------------------------------------------
# Value — virtual register / SSA variable
# ---------------------------------------------------------------------------

@dataclass
class Value:
    """A virtual register representing a single definition in the MIR.

    Attributes
    ----------
    id : int
        Unique numeric identifier.  Two Values with the same ``id`` are
        considered identical (see ``__eq__`` / ``__hash__``).
    data_type : str
        Type annotation (default ``"Any"``).  Used downstream by the type
        checker and LLVM backend.
    defining_inst : MIRInstruction | None
        Back-pointer to the instruction that produces this value.
        ``None`` for function parameters and PHI-inserted values before
        linking.
    name : str | None
        Optional debug / display name (e.g. the original variable name
        before SSA renaming).
    """

    id: int
    data_type: str = "Any"
    defining_inst: Optional['MIRInstruction'] = field(default=None, repr=False)
    name: Optional[str] = None

    # ------------------------------------------------------------------
    # Identity is based *only* on the numeric id.
    #
    # Why:  ``@dataclass`` auto-generates __eq__ that compares ALL fields,
    # including mutable ``defining_inst``.  That breaks set/dict lookups
    # because two Values with the same id but different back-pointers
    # would be treated as different — a subtle, hard-to-debug corruption.
    # ------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Value):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"%{self.id}"


# ---------------------------------------------------------------------------
# MIR Nodes
# ---------------------------------------------------------------------------

@dataclass
class MIRNode:
    """Base class for all Mid-level IR nodes."""
    pass


@dataclass
class MIRInstruction(MIRNode):
    """A single three-address-code instruction.

    Examples
    --------
    ::

        %3 = BINARY_+ %1, %2      →  MIRInstruction("BINARY_+", [val1, val2], result=val3)
        STORE_VAR "x", %1          →  MIRInstruction("STORE_VAR", ["x", val1])
        %5 = CONST 42              →  MIRInstruction("CONST", [42], result=val5)

    Attributes
    ----------
    opcode : str
        The operation name (e.g. ``"CONST"``, ``"BINARY_+"``, ``"CALL"``).
    operands : list[Any]
        Positional operands — may be ``Value`` objects, literals, or strings.
    result : Value | None
        The value defined by this instruction (``None`` for side-effect-only
        instructions like ``STORE_VAR`` or ``PRINT``).
    """

    opcode: str
    operands: List[Any]
    result: Optional[Value] = None


# ---------------------------------------------------------------------------
# LEGACY nodes — unused in the new SSA pipeline (R4+).
# Kept temporarily for backward compatibility with older tests / tooling.
# TODO(R4.5): Remove once legacy pipeline is fully retired.
# ---------------------------------------------------------------------------

@dataclass
class MIRCreateArray(MIRNode):
    """LEGACY: Array creation node from the pre-CFG pipeline."""
    elements: List[MIRNode]


@dataclass
class MIRLoop(MIRNode):
    """LEGACY: Loop node from the pre-CFG pipeline."""
    iterator: str
    iterable: MIRNode
    body: List[MIRNode]
