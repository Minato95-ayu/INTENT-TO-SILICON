"""
compiler.ir.dominators — Dominator analysis pass
=================================================

Computes three fundamental properties of a CFG that are required for
SSA construction (Cytron et al., 1991):

1. **DOM sets**         — ``DOM(n)`` = set of all blocks that dominate ``n``.
2. **Immediate dominator** — ``idom(n)`` = the closest strict dominator of ``n``.
3. **Dominance frontier**  — ``DF(n)`` = set of blocks where ``n``'s dominance
   "stops" — i.e. join points where a PHI node may be needed.

Algorithm
---------
- DOM sets are computed using the classic iterative data-flow algorithm
  (cf. Appel, *Modern Compiler Implementation*, §19.1).
- idom is derived from DOM sets by finding the strict dominator that is
  dominated by all other strict dominators.
- DF is computed using the "bottom-up" algorithm from Cytron et al.

Complexity
----------
- ``_compute_doms``: O(n² · E) in the worst case (iterative fixed-point).
  Acceptable for functions with < ~1000 blocks.
- ``_compute_idom``: O(n³) worst case — quadratic per block.
- ``_compute_df``:   O(n · E).

For very large CFGs, consider switching to the Cooper–Harvey–Kennedy (2001)
algorithm which computes idom in near-linear time O(n · α(n)).

See Also
--------
compiler.ir.ssa : SSA construction pass that consumes the DominatorTree.
"""

from typing import Dict, Set

from compiler.ir.mir_cfg import CFG, BasicBlock


class DominatorTree:
    """Computes and stores dominator information for a CFG.

    On construction, all three analyses (DOM, idom, DF) are computed
    eagerly.  Results are stored in public attributes for downstream
    consumption by the SSA builder.

    Attributes
    ----------
    cfg : CFG
        The control-flow graph being analyzed (not mutated).
    doms : dict[BasicBlock, set[BasicBlock]]
        ``doms[n]`` = the set of all blocks that dominate block ``n``
        (including ``n`` itself).
    idom : dict[BasicBlock, BasicBlock]
        ``idom[n]`` = the immediate dominator of ``n``.
        The entry block has no entry in this dict.
    df : dict[BasicBlock, set[BasicBlock]]
        ``df[n]`` = the dominance frontier of block ``n`` — i.e. the set
        of blocks where a PHI node may be needed for variables defined
        in ``n``.

    Example
    -------
    ::

        dt = DominatorTree(cfg)
        assert entry in dt.doms[then_block]   # entry dominates then
        assert dt.idom[then_block] == entry    # entry is immediate dominator
        assert merge in dt.df[then_block]      # merge is in then's DF
    """

    def __init__(self, cfg: CFG):
        self.cfg = cfg
        self.doms: Dict[BasicBlock, Set[BasicBlock]] = {}
        self.idom: Dict[BasicBlock, BasicBlock] = {}
        self.df: Dict[BasicBlock, Set[BasicBlock]] = {}

        self._compute_doms()
        self._compute_idom()
        self._compute_df()

    # ------------------------------------------------------------------
    # Pass 1: Iterative dominator set computation
    # ------------------------------------------------------------------

    def _compute_doms(self) -> None:
        """Compute DOM(n) for every block using iterative data-flow.

        Algorithm::

            DOM(entry) = {entry}
            DOM(n)     = {n} ∪ ⋂ { DOM(p) | p ∈ preds(n) }

        Iterates until no DOM set changes (fixed-point).
        """
        all_nodes = set(self.cfg.blocks)
        entry = self.cfg.entry_block

        # Initialize: entry dominates only itself; all others start as
        # the universal set (optimistic initialization).
        for block in self.cfg.blocks:
            if block == entry:
                self.doms[block] = {entry}
            else:
                self.doms[block] = set(all_nodes)

        changed = True
        while changed:
            changed = False
            for block in self.cfg.blocks:
                if block == entry:
                    continue

                preds = block.predecessors
                if not preds:
                    # Unreachable block — dominates only itself.
                    new_dom = {block}
                else:
                    # Intersect all predecessors' DOM sets, then add self.
                    new_dom = set(self.doms[preds[0]])
                    for pred in preds[1:]:
                        new_dom &= self.doms[pred]
                    new_dom.add(block)

                if new_dom != self.doms[block]:
                    self.doms[block] = new_dom
                    changed = True

    # ------------------------------------------------------------------
    # Pass 2: Immediate dominator extraction
    # ------------------------------------------------------------------

    def _compute_idom(self) -> None:
        """Derive idom(n) from the DOM sets.

        The immediate dominator of ``n`` is the strict dominator of ``n``
        that does **not** strictly dominate any other strict dominator of
        ``n``.  Equivalently, it is the "closest" dominator.
        """
        entry = self.cfg.entry_block

        for block in self.cfg.blocks:
            if block == entry:
                continue

            strict_doms = self.doms[block] - {block}
            if not strict_doms:
                continue

            # Find the strict dominator that is dominated by ALL others.
            for candidate in strict_doms:
                is_immediate = True
                for other in strict_doms:
                    if candidate == other:
                        continue
                    # If candidate strictly dominates other, it's "farther"
                    # from block — so it's not the immediate one.
                    if candidate in (self.doms[other] - {other}):
                        is_immediate = False
                        break

                if is_immediate:
                    self.idom[block] = candidate
                    break

    # ------------------------------------------------------------------
    # Pass 3: Dominance frontier computation
    # ------------------------------------------------------------------

    def _compute_df(self) -> None:
        """Compute the dominance frontier for every block.

        Algorithm (from Cytron et al.)::

            For each join point b (≥ 2 predecessors):
                For each predecessor p of b:
                    runner = p
                    while runner ≠ idom(b):
                        DF(runner) ∪= {b}
                        runner = idom(runner)
        """
        # Initialize empty DF sets.
        for block in self.cfg.blocks:
            self.df[block] = set()

        for block in self.cfg.blocks:
            if len(block.predecessors) < 2:
                continue  # Only join points generate DF entries.

            for pred in block.predecessors:
                runner = pred
                while runner != self.idom.get(block):
                    if runner is None:
                        break  # Safety: unreachable / disconnected graph.
                    self.df[runner].add(block)
                    runner = self.idom.get(runner)
