from typing import Dict, Set, List
from aayu.compiler.mir.nodes import FunctionMIR, BasicBlock
from aayu.compiler.pass_manager import AnalysisPass

class DominatorTreePass(AnalysisPass):
    """
    Computes Immediate Dominators (idom) and Dominance Frontiers (DF)
    for a given FunctionMIR.
    """
    def __init__(self):
        self.dom: Dict[str, Set[str]] = {}
        self.idom: Dict[str, str] = {}
        self.df: Dict[str, Set[str]] = {}
        self.dom_tree_children: Dict[str, List[str]] = {}

    def run(self, func: FunctionMIR) -> FunctionMIR:
        if not func.blocks:
            return func
            
        self._compute_dominators(func)
        self._compute_idom(func)
        self._compute_dom_tree(func)
        self._compute_dominance_frontier(func)
        
        # Store analysis results on the function object for subsequent passes
        func.analysis = getattr(func, 'analysis', {})
        func.analysis['dom'] = self.dom
        func.analysis['idom'] = self.idom
        func.analysis['df'] = self.df
        func.analysis['dom_tree'] = self.dom_tree_children
        
        return func

    def _compute_dominators(self, func: FunctionMIR):
        all_nodes = {b.id for b in func.blocks}
        self.dom = {b.id: set(all_nodes) for b in func.blocks}
        entry = func.entry_block.id
        self.dom[entry] = {entry}
        
        changed = True
        while changed:
            changed = False
            for b in func.blocks:
                if b.id == entry:
                    continue
                    
                # Intersect dominators of all predecessors
                new_dom = None
                for p in b.predecessors:
                    if new_dom is None:
                        new_dom = set(self.dom[p.id])
                    else:
                        new_dom = new_dom.intersection(self.dom[p.id])
                        
                if new_dom is None:
                    new_dom = set()
                    
                new_dom.add(b.id)
                
                if new_dom != self.dom[b.id]:
                    self.dom[b.id] = new_dom
                    changed = True

    def _compute_idom(self, func: FunctionMIR):
        self.idom = {}
        for b in func.blocks:
            strict_doms = self.dom[b.id] - {b.id}
            if not strict_doms:
                continue
                
            # idom is the strict dominator that is dominated by all other strict dominators
            # Effectively, it's the strict dominator with the largest dom set
            candidate = None
            max_size = -1
            for d in strict_doms:
                if len(self.dom[d]) > max_size:
                    candidate = d
                    max_size = len(self.dom[d])
            self.idom[b.id] = candidate

    def _compute_dom_tree(self, func: FunctionMIR):
        self.dom_tree_children = {b.id: [] for b in func.blocks}
        for node, imm_dom in self.idom.items():
            if imm_dom:
                self.dom_tree_children[imm_dom].append(node)

    def _compute_dominance_frontier(self, func: FunctionMIR):
        self.df = {b.id: set() for b in func.blocks}
        
        for b in func.blocks:
            if len(b.predecessors) >= 2:
                for p in b.predecessors:
                    runner = p.id
                    # walk up the dominator tree until we hit the immediate dominator of b
                    while runner != self.idom.get(b.id, None):
                        if runner is None:
                            break
                        self.df[runner].add(b.id)
                        runner = self.idom.get(runner, None)

    def verify(self, func: FunctionMIR) -> bool:
        return True
