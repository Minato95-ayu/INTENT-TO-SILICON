"""
compiler.ir.optimizer — SSA-based optimization passes
=====================================================

Implements a fixed-point optimization loop on an SSA-form CFG.  Each
iteration runs the following passes in order:

1. **Constant Propagation + Folding** — replaces Value operands with
   known literal values, then folds pure arithmetic into compile-time
   constants.
2. **Dead Code Elimination (DCE)** — removes instructions whose result
   has zero uses *and* that have no side effects.

The loop repeats until a full cycle produces zero mutations (fixed point).
This ensures that newly exposed opportunities (e.g. a fold enabling a
new DCE) are always captured.

Safety invariant
----------------
Instructions with **side effects** (``CALL``, ``PRINT``, ``STORE``,
``ACTION_DECL``) are **never** removed by DCE, even if their result
Value has zero uses.  Only opcodes in ``PURE_OPCODES`` are candidates
for elimination.

Division semantics
------------------
Constant folding uses Python's ``/`` operator, which returns a ``float``
for integer operands (e.g. ``10 / 5 → 2.0``).  If AAYU's integer
division semantics differ, this should be updated to use ``//`` for
integer operands.  Division by zero is handled gracefully (the fold is
skipped).

See Also
--------
compiler.ir.ssa        : SSA construction pass (runs before this).
compiler.ir.linearizer : Out-of-SSA lowering (runs after this).
"""

from typing import Any, Dict

from compiler.ir.mir_cfg import CFG, BasicBlock, Branch, Jump, Return
from compiler.ir.mir import MIRInstruction, Value


class SSAOptimizer:
    """Fixed-point optimizer operating on an SSA-form CFG.

    Usage::

        SSAOptimizer(cfg).optimize()
        # cfg is now optimized (mutated in place).

    Parameters
    ----------
    cfg : CFG
        The SSA-form CFG to optimize (mutated in place).
    """

    # Opcodes that are guaranteed to have no side effects.  Only these
    # (plus PHI) are candidates for dead-code elimination.
    #
    # Note: LOAD_VAR is intentionally excluded because it should have been
    # eliminated by the SSA pass.  If it appears here, it indicates a bug
    # in the SSA builder.
    PURE_OPCODES = frozenset({
        "CONST",
        "BINARY_+", "BINARY_-", "BINARY_*", "BINARY_/",
        "BINARY_==", "BINARY_!=", "BINARY_<", "BINARY_<=",
        "BINARY_>", "BINARY_>=",
        "UNARY_!", "UNARY_-",
        "CAST",
        "COPY",
    })

    def __init__(self, cfg: CFG):
        self.cfg = cfg
        self._changed = False  # Tracks whether the current iteration mutated anything.

    def optimize(self) -> None:
        """Run all optimization passes in a fixed-point loop.

        Repeats until a full cycle produces no mutations.
        """
        while True:
            self._changed = False
            self._pass_constant_fold_propagate()
            self._pass_dce()
            if not self._changed:
                break

    # ------------------------------------------------------------------
    # Pass 1: Constant propagation + folding
    # ------------------------------------------------------------------

    def _pass_constant_fold_propagate(self) -> None:
        """Propagate known constants and fold pure arithmetic.

        Two sub-steps per block:

        A. **Propagation** — if an operand is a ``Value`` whose defining
           instruction is ``CONST``, replace the operand with the literal.
        B. **Folding** — if all operands of a pure binary instruction are
           now literals, evaluate the operation at compile time and rewrite
           the instruction to ``CONST``.

        PHI nodes are intentionally skipped for propagation because folding
        them requires CFG simplification (unreachable-branch removal),
        which is a separate pass.
        """
        # Collect all known constants: Value.id → literal value.
        constants: Dict[int, Any] = {}
        for block in self.cfg.blocks:
            for inst in block.instructions:
                if inst.opcode == "CONST" and inst.result is not None:
                    constants[inst.result.id] = inst.operands[0]

        # Propagate and fold.
        for block in self.cfg.blocks:
            for inst in block.instructions:
                # A. Propagate constants into operands (skip PHI).
                if inst.opcode != "PHI":
                    for i in range(len(inst.operands)):
                        op = inst.operands[i]
                        if isinstance(op, Value) and op.id in constants:
                            inst.operands[i] = constants[op.id]
                            self._changed = True

                # B. Constant folding for binary operations.
                if (inst.opcode.startswith("BINARY_")
                        and len(inst.operands) == 2):
                    left, right = inst.operands
                    if not isinstance(left, Value) and \
                       not isinstance(right, Value):
                        folded = self._try_fold(inst.opcode, left, right)
                        if folded is not None:
                            inst.opcode = "CONST"
                            inst.operands = [folded]
                            if inst.result is not None:
                                constants[inst.result.id] = folded
                            self._changed = True

            # Propagate constants into terminators.
            term = block.terminator
            if (isinstance(term, Branch)
                    and isinstance(term.condition, Value)
                    and term.condition.id in constants):
                term.condition = constants[term.condition.id]
                self._changed = True
            elif (isinstance(term, Return)
                  and isinstance(term.value, Value)
                  and term.value.id in constants):
                term.value = constants[term.value.id]
                self._changed = True

    @staticmethod
    def _try_fold(opcode: str, left: Any, right: Any) -> Any:
        """Attempt to evaluate a binary operation at compile time.

        Returns
        -------
        Any
            The folded result, or ``None`` if folding is not possible
            (e.g. type mismatch, division by zero).
        """
        op = opcode[7:]  # Strip "BINARY_" prefix.
        try:
            if op == "+":   return left + right
            if op == "-":   return left - right
            if op == "*":   return left * right
            if op == "/":
                if right == 0:
                    return None  # Division by zero — skip fold.
                return left / right
            if op == "==":  return left == right
            if op == "!=":  return left != right
            if op == "<":   return left < right
            if op == "<=":  return left <= right
            if op == ">":   return left > right
            if op == ">=":  return left >= right
        except Exception:
            return None  # Type error or other runtime issue — skip fold.
        return None

    # ------------------------------------------------------------------
    # Pass 2: Dead code elimination (DCE)
    # ------------------------------------------------------------------

    def _pass_dce(self) -> None:
        """Remove instructions whose result is unused and side-effect-free.

        Algorithm:
        1. Count global uses of every ``Value`` across all instructions,
           PHI operands, and terminators.
        2. For each instruction with a result that has **zero uses**:
           - If the opcode is in ``PURE_OPCODES`` or is ``"PHI"``, remove it.
           - Otherwise (CALL, PRINT, STORE, etc.), **keep it** — it has
             observable side effects.
        """
        # -- Step 1: Count uses globally -----------------------------------

        uses: Dict[int, int] = {}

        # Initialize counters for all defined Values.
        for block in self.cfg.blocks:
            for inst in block.instructions:
                if inst.result is not None:
                    uses[inst.result.id] = 0

        # Count references in instruction operands.
        for block in self.cfg.blocks:
            for inst in block.instructions:
                if inst.opcode == "PHI":
                    # PHI operands are {predecessor: Value} dicts.
                    phi_dict = inst.operands[0]
                    for val in phi_dict.values():
                        if isinstance(val, Value) and val.id in uses:
                            uses[val.id] += 1
                else:
                    for op in inst.operands:
                        if isinstance(op, Value) and op.id in uses:
                            uses[op.id] += 1

            # Count references in terminators.
            term = block.terminator
            if (isinstance(term, Branch)
                    and isinstance(term.condition, Value)
                    and term.condition.id in uses):
                uses[term.condition.id] += 1
            elif (isinstance(term, Return)
                  and isinstance(term.value, Value)
                  and term.value.id in uses):
                uses[term.value.id] += 1

        # -- Step 2: Prune dead instructions --------------------------------

        for block in self.cfg.blocks:
            survivors = []
            for inst in block.instructions:
                is_dead = False

                if (inst.result is not None
                        and uses.get(inst.result.id, 0) == 0):
                    # Result has no uses — safe to remove if pure.
                    if (inst.opcode in self.PURE_OPCODES
                            or inst.opcode == "PHI"):
                        is_dead = True

                if is_dead:
                    self._changed = True
                else:
                    survivors.append(inst)

            block.instructions = survivors
