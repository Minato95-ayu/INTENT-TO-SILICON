from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional

class RegisterClass(Enum):
    GENERAL = auto()
    FLOAT = auto()
    VECTOR = auto()
    SPECIAL = auto()

@dataclass(frozen=True)
class PhysicalRegister:
    id: int
    name: str
    kind: RegisterClass
    width: int
    reserved: bool = False
    callee_saved: bool = False

    def __str__(self) -> str:
        return self.name

@dataclass
class LiveInterval:
    register_id: int
    start: int = -1
    end: int = -1
    uses: List[int] = field(default_factory=list)
    weight: float = 1.0 # Base weight outside loop
    spill_cost: float = 0.0
    loop_depth: int = 0
    frequency: float = 1.0
    assigned_register: Optional[PhysicalRegister] = None
    spill_slot: Optional[int] = None
    
    def compute_spill_cost(self):
        # spill_cost = (uses * loop_weight * frequency) / live_length
        # loop_weight = 10^loop_depth
        length = max(1, self.end - self.start)
        use_count = len(self.uses)
        loop_weight = 10 ** self.loop_depth
        self.spill_cost = (use_count * loop_weight * self.frequency * self.weight) / length
        
    def add_use(self, index: int):
        if index not in self.uses:
            self.uses.append(index)
            # Update start/end
            if self.start == -1 or index < self.start:
                self.start = index
            if self.end == -1 or index > self.end:
                self.end = index

    def __str__(self):
        assigned = self.assigned_register.name if self.assigned_register else ("SPILL" if self.spill_slot is not None else "UNASSIGNED")
        return f"LiveInterval(r{self.register_id}: [{self.start}, {self.end}], uses={len(self.uses)}, cost={self.spill_cost:.2f}) -> {assigned}"
