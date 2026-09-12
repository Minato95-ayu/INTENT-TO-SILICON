"""
compiler.ir.ssa — SSA construction pass (Cytron et al., 1991)
=============================================================

Transforms a CFG with explicit ``LOAD_VAR`` / ``STORE_VAR`` instructions
into Static Single Assignment (SSA) form by:

1. **PHI placement** — inserting PHI nodes at the iterated dominance
   frontier (DF⁺) of each variable's definition sites.
2. **Variable renaming** — performing a dominator-tree DFS to version
   each variable and rewrite all uses to refer to the correct version.

After this pass:
- Every ``LOAD_VAR`` and ``STORE_VAR`` instruction is **eliminated**.
- All data flow is explicit through ``Value`` objects and ``PHI`` nodes.
- The CFG is in valid SSA form, ready for optimization.

References
----------
- R. Cytron, J. Ferrante, B. K. Rosen, M. N. Wegman, F. K. Zadeck,
  "Efficiently Computing Static Single Assignment Form and the Control
  Dependence Graph," ACM TOPLAS, 1991.

See Also
--------
compiler.ir.dominators : DominatorTree that this pass depends on.
compiler.ir.optimizer  : SSA-based optimization passes.
"""

from typing import Dict, List, Set
from collections import defaultdict

from compiler.ir.mir_cfg import CFG, BasicBlock, Branch, Jump, Return
from compiler.ir.mir import MIRInstruction, Value
from compiler.ir.dominators import DominatorTree


# Sentinel value id for undefined variables.  Uses a large negative number
# to avoid collision with any real Value id (which start at 1).
_UNDEF_VALUE_ID = -9999


class SSABuilder:
    """Converts a CFG from named-variable form to SSA form.

    Usage::

        dom_tree = DominatorTree(cfg)
        SSABuilder(cfg, dom_tree).build()
        # cfg is now in SSA form (mutated in place).

    Parameters
    ----------
    cfg : CFG
        The control-flow graph to transform (mutated in place).
    dom_tree : DominatorTree
        Pre-computed dominator information for ``cfg``.
    """

    def __init__(self, cfg: CFG, dom_tree: DominatorTree):
        self.cfg = cfg
        self.dt = dom_tree

        # Start value counter above the highest existing Value id to
        # avoid collisions with ids created by the CFG builder.
        self.value_counter: int = max(
            (inst.result.id
             for block in cfg.blocks
             for inst in block.instructions
             if inst.result is not None),
            default=0,
        )

    def _next_value(self) -> Value:
        """Allocate a fresh Value with a unique id."""
        self.value_counter += 1
        return Value(id=self.value_counter)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self) -> None:
        """Run the full SSA construction algorithm.

        Mutates ``self.cfg`` in place:
        1. Inserts PHI nodes at dominance frontiers.
        2. Renames all variable references via dominator-tree DFS.
        3. Removes all ``LOAD_VAR`` and ``STORE_VAR`` instructions.
        """
        # Step 1: Find all variable definition sites.
        def_blocks: Dict[str, Set[BasicBlock]] = defaultdict(set)
        for block in self.cfg.blocks:
            for inst in block.instructions:
                if inst.opcode == "STORE_VAR":
                    var_name = inst.operands[0]
                    def_blocks[var_name].add(block)

        # Step 2: Insert PHI nodes at iterated dominance frontiers.
        phi_nodes: Dict[BasicBlock, Dict[str, MIRInstruction]] = \
            defaultdict(dict)

        for var_name, blocks in def_blocks.items():
            worklist = list(blocks)
            has_phi: Set[BasicBlock] = set()

            while worklist:
                block = worklist.pop(0)
                for df_block in self.dt.df.get(block, set()):
                    if df_block not in has_phi:
                        # Create PHI: result = PHI({pred1: val1, ...})
                        phi_val = self._next_value()
                        phi_inst = MIRInstruction(
                            opcode="PHI", operands=[{}])
                        phi_inst.result = phi_val
                        phi_val.defining_inst = phi_inst

                        df_block.instructions.insert(0, phi_inst)
                        phi_nodes[df_block][var_name] = phi_inst
                        has_phi.add(df_block)

                        # A PHI is itself a new definition — propagate.
                        if df_block not in def_blocks[var_name]:
                            worklist.append(df_block)

        # Step 3: Rename variables via dominator-tree DFS.
        self._rename(phi_nodes)

    # ------------------------------------------------------------------
    # Renaming
    # ------------------------------------------------------------------

    def _rename(
        self,
        phi_nodes: Dict[BasicBlock, Dict[str, MIRInstruction]],
    ) -> None:
        """Rename all variable uses via dominator-tree DFS.

        Each variable maintains a version stack.  On entering a block,
        new definitions push onto the stack; on leaving, they are popped
        so sibling subtrees see the correct version.
        """
        # Per-variable version stack.
        stacks: Dict[str, List[Value]] = defaultdict(list)

        def get_active(var: str) -> Value:
            """Return the currently active Value for *var*.

            If the variable has no active definition (e.g. used before
            assignment), return a sentinel UNDEF value.  This should
            have been caught by the semantic analyzer, but we handle it
            gracefully to avoid crashes.
            """
            if stacks[var]:
                return stacks[var][-1]
            return Value(id=_UNDEF_VALUE_ID, name=f"undef_{var}")

        def rename_block(block: BasicBlock) -> None:
            """Process one block and recurse into dominated children."""
            # Track how many values we push per variable so we can pop
            # them when backtracking.
            pushed_counts: Dict[str, int] = defaultdict(int)

            # Per-block replacement map: old Value.id → new Value.
            # Scoped to THIS block to avoid cross-branch contamination.
            # (Fix #17: previously this was shared across the entire DFS,
            #  which caused incorrect replacements in sibling branches.)
            local_replacements: Dict[int, Value] = {}

            # -- Phase 1: Process instructions in this block ----------------

            instructions_to_keep: List[MIRInstruction] = []

            for inst in block.instructions:
                if inst.opcode == "PHI":
                    # PHI defines a new version of its variable.
                    var_name = None
                    for v, p_inst in phi_nodes[block].items():
                        if p_inst is inst:
                            var_name = v
                            break
                    if var_name:
                        stacks[var_name].append(inst.result)
                        pushed_counts[var_name] += 1
                    instructions_to_keep.append(inst)

                elif inst.opcode == "LOAD_VAR":
                    # Replace with the active Value for this variable.
                    var_name = inst.operands[0]
                    active_val = get_active(var_name)
                    local_replacements[inst.result.id] = active_val
                    # Drop LOAD_VAR — it's replaced by direct Value flow.

                elif inst.opcode == "STORE_VAR":
                    # Push the stored value as the new version.
                    var_name = inst.operands[0]
                    val = inst.operands[1]
                    # Resolve if the stored value itself was a LOAD_VAR.
                    if isinstance(val, Value) and val.id in local_replacements:
                        val = local_replacements[val.id]
                    stacks[var_name].append(val)
                    pushed_counts[var_name] += 1
                    # Drop STORE_VAR — SSA doesn't need it.

                else:
                    # Rewrite operands that reference replaced Values.
                    for i in range(len(inst.operands)):
                        op = inst.operands[i]
                        if (isinstance(op, Value)
                                and op.id in local_replacements):
                            inst.operands[i] = local_replacements[op.id]
                    instructions_to_keep.append(inst)

            block.instructions = instructions_to_keep

            # -- Phase 2: Rewrite terminator operands -----------------------

            term = block.terminator
            if (isinstance(term, Branch)
                    and isinstance(term.condition, Value)
                    and term.condition.id in local_replacements):
                term.condition = local_replacements[term.condition.id]
            elif (isinstance(term, Return)
                  and isinstance(term.value, Value)
                  and term.value.id in local_replacements):
                term.value = local_replacements[term.value.id]

            # -- Phase 3: Fill successors' PHI operands ---------------------

            for succ in block.successors:
                for var_name, phi_inst in phi_nodes[succ].items():
                    if stacks[var_name]:
                        phi_dict = phi_inst.operands[0]
                        phi_dict[block] = stacks[var_name][-1]

            # -- Phase 4: Recurse into dominated children -------------------

            children = [c for c in self.cfg.blocks
                        if self.dt.idom.get(c) is block]
            for child in children:
                rename_block(child)

            # -- Phase 5: Pop stacks (backtrack) ----------------------------

            for var_name, count in pushed_counts.items():
                for _ in range(count):
                    stacks[var_name].pop()

        # Start DFS from the entry block.
        rename_block(self.cfg.entry_block)
