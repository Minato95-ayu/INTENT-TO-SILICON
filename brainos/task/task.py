from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"

@dataclass
class Task:
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "metadata": self.metadata
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        return cls(
            id=data["id"],
            description=data["description"],
            status=TaskStatus(data.get("status", "PENDING")),
            dependencies=data.get("dependencies", []),
            metadata=data.get("metadata", {})
        )
