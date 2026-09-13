import re
with open('compiler/ir/mir_cfg.py', 'r') as f:
    content = f.read()

replacement = """@dataclass
class BasicBlock:
    \"\"\"A linear sequence of instructions ending in exactly one terminator.\"\"\"
    id: str
    instructions: List[MIRInstruction] = field(default_factory=list)
    terminator: Optional[Terminator] = None
    predecessors: List['BasicBlock'] = field(default_factory=list)
    successors: List['BasicBlock'] = field(default_factory=list)
    
    def __hash__(self):
        return hash(self.id)
        
    def __eq__(self, other):
        if not isinstance(other, BasicBlock): return False
        return self.id == other.id
"""

content = re.sub(r'@dataclass\nclass BasicBlock:.*?(?=\s+def set_terminator)', replacement, content, flags=re.DOTALL)

with open('compiler/ir/mir_cfg.py', 'w') as f:
    f.write(content)
