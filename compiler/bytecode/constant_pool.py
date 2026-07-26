from dataclasses import dataclass
from typing import Any, List

@dataclass
class ConstantEntry:
    """A typed entry in the constant pool."""
    type: str   # "INT", "STRING", "BOOL", "FLOAT"
    value: Any

    def serialize(self):
        return (self.type, self.value)

class ConstantPool:
    """Typed constant pool for the AAYU bytecode format.
    
    Each entry stores a type tag and value, enabling future
    serialization and type-safe constant access at runtime.
    """
    def __init__(self):
        self.entries: List[ConstantEntry] = []
        self._index_cache: dict = {}  # (type, value) -> index

    def add(self, value: Any) -> int:
        """Add a value to the constant pool. Returns its index.
        Deduplicates identical (type, value) pairs.
        """
        type_tag = self._infer_type(value)
        if isinstance(value, dict):
            key_val = str(sorted([(k, str(v)) for k, v in value.items()]))
        elif isinstance(value, list):
            key_val = str(value)
        else:
            key_val = value
        key = (type_tag, key_val)

        if key in self._index_cache:
            return self._index_cache[key]

        idx = len(self.entries)
        self.entries.append(ConstantEntry(type=type_tag, value=value))
        self._index_cache[key] = idx
        return idx

    def get(self, index: int) -> ConstantEntry:
        """Retrieve a constant by index."""
        if index < 0 or index >= len(self.entries):
            raise IndexError(f"Constant pool index out of bounds: {index}")
        return self.entries[index]

    def __getitem__(self, index: int) -> Any:
        return self.entries[index].value

    def size(self) -> int:
        return len(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def values(self) -> List[Any]:
        """Return raw values list for VM consumption."""
        return [e.value for e in self.entries]

    @staticmethod
    def _infer_type(value: Any) -> str:
        if isinstance(value, bool):
            return "BOOL"
        elif isinstance(value, int):
            return "INT"
        elif isinstance(value, float):
            return "FLOAT"
        elif isinstance(value, str):
            return "STRING"
        elif isinstance(value, dict):
            return "DICT"
        else:
            return "STRING"  # fallback: serialize as string

    def __repr__(self):
        lines = []
        for i, entry in enumerate(self.entries):
            lines.append(f"  {i:4d} {entry.type:8s} {entry.value!r}")
        return "ConstantPool:\n" + "\n".join(lines)
