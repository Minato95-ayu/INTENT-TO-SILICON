from dataclasses import dataclass, field
from typing import List, Set, Optional
from .instructions import Instruction

@dataclass
class BasicBlock:
    """A Basic Block in the Control Flow Graph"""
    id: str
    instructions: List[Instruction] = field(default_factory=list)
    predecessors: List['BasicBlock'] = field(default_factory=list)
    successors: List['BasicBlock'] = field(default_factory=list)
    
    # Analysis metadata
    dominators: Set['BasicBlock'] = field(default_factory=set)
    post_dominators: Set['BasicBlock'] = field(default_factory=set)
    live_in: Set[str] = field(default_factory=set)
    live_out: Set[str] = field(default_factory=set)
    
    def __hash__(self):
        return hash(self.id)
        
    def __eq__(self, other):
        if not isinstance(other, BasicBlock):
            return False
        return self.id == other.id

@dataclass
class ControlFlowGraph:
    """The Control Flow Graph for a function or module"""
    name: str
    entry: BasicBlock
    exit: BasicBlock
    blocks: List[BasicBlock] = field(default_factory=list)
    
    def add_block(self, block: BasicBlock):
        if block not in self.blocks:
            self.blocks.append(block)

    def add_edge(self, from_block: BasicBlock, to_block: BasicBlock):
        if to_block not in from_block.successors:
            from_block.successors.append(to_block)
        if from_block not in to_block.predecessors:
            to_block.predecessors.append(from_block)
