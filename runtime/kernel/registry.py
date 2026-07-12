import threading
import logging
from typing import Dict, List
from .interface import RuntimeInterface

logger = logging.getLogger("aayu.kernel")

class RuntimeRegistry:
    """
    Thread-safe registry for managing AAYU Runtime plugins.
    """
    def __init__(self):
        self._lock = threading.RLock()
        self._runtimes: Dict[str, RuntimeInterface] = {}

    def register(self, runtime: RuntimeInterface) -> None:
        """Register a new runtime plugin."""
        metadata = runtime.metadata()
        with self._lock:
            if metadata.name in self._runtimes:
                raise ValueError(f"Runtime '{metadata.name}' is already registered.")
            self._runtimes[metadata.name] = runtime
            logger.info(f"Registered runtime: {metadata.name} v{metadata.version}")

    def get(self, name: str) -> RuntimeInterface:
        """Fetch a registered runtime by name. Returns None if not found."""
        with self._lock:
            return self._runtimes.get(name)

    def remove(self, name: str) -> None:
        """Remove a runtime from the registry."""
        with self._lock:
            if name in self._runtimes:
                del self._runtimes[name]
                logger.info(f"Unregistered runtime: {name}")

    def list_all(self) -> List[RuntimeInterface]:
        """Return a list of all registered runtimes."""
        with self._lock:
            return list(self._runtimes.values())

    def get_boot_order(self) -> List[RuntimeInterface]:
        """
        Sort runtimes based on their declared dependencies (Topological Sort).
        Returns a list of runtimes in the correct boot order.
        """
        with self._lock:
            visited = set()
            temp_marks = set()
            order = []

            def visit(name: str):
                if name in temp_marks:
                    raise RuntimeError(f"Circular dependency detected involving runtime: {name}")
                if name not in visited:
                    temp_marks.add(name)
                    plugin = self._runtimes.get(name)
                    if plugin:
                        for dep in plugin.metadata().dependencies:
                            visit(dep)
                        order.append(plugin)
                    temp_marks.remove(name)
                    visited.add(name)

            for name in self._runtimes:
                if name not in visited:
                    visit(name)
            
            return order
