import threading
import copy
from typing import Any, Dict, List

class StateStore:
    """
    Thread-safe, deeply nested dictionary for State Runtime.
    Supports deep paths like 'user.address.city'.
    """
    def __init__(self):
        self._lock = threading.RLock()
        self._state: Dict[str, Any] = {}

    def _parse_path(self, path: str) -> List[str]:
        if not path:
            return []
        return path.split(".")

    def set(self, path: str, value: Any) -> None:
        with self._lock:
            keys = self._parse_path(path)
            if not keys:
                raise ValueError("Path cannot be empty")
            
            # Navigate to the correct depth, creating dicts if necessary
            current = self._state
            for key in keys[:-1]:
                if key not in current or not isinstance(current[key], dict):
                    current[key] = {}
                current = current[key]
                
            current[keys[-1]] = copy.deepcopy(value)

    def get(self, path: str) -> Any:
        with self._lock:
            keys = self._parse_path(path)
            if not keys:
                return copy.deepcopy(self._state)
                
            current = self._state
            for key in keys:
                if not isinstance(current, dict) or key not in current:
                    raise KeyError(f"Path not found: {path}")
                current = current[key]
                
            return copy.deepcopy(current)

    def remove(self, path: str) -> None:
        with self._lock:
            keys = self._parse_path(path)
            if not keys:
                self._state = {}
                return
                
            current = self._state
            for key in keys[:-1]:
                if not isinstance(current, dict) or key not in current:
                    raise KeyError(f"Path not found: {path}")
                current = current[key]
                
            if keys[-1] in current:
                del current[keys[-1]]
            else:
                raise KeyError(f"Path not found: {path}")

    def snapshot(self) -> Dict[str, Any]:
        """Returns a deep-copied immutable snapshot of the entire state."""
        with self._lock:
            return copy.deepcopy(self._state)

    def restore(self, snapshot: Dict[str, Any]) -> None:
        """Restores the state from a deep-copied snapshot."""
        with self._lock:
            self._state = copy.deepcopy(snapshot)
