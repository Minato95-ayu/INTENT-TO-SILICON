"""
AAYU Operating System - Plugin Registry
---------------------------------------
File: runtime/kernel/registry.py

WHY DOES THIS FILE EXIST?
AAYU OS uses a decoupled, microkernel architecture. The VM should never instantiate 
runtimes directly (e.g. `StorageRuntime()`). Instead, runtimes are registered here.

WHAT DOES THIS CODE DO?
1. Thread Safety: Using `threading.RLock`, it ensures that if multiple async tasks 
   try to query or register plugins simultaneously, the system won't corrupt memory.
2. Topological Sort (`get_boot_order`): This is the most critical function. If the UI 
   Runtime depends on the State Runtime, UI *cannot* boot before State. This algorithm 
   builds a directed acyclic graph (DAG) of dependencies and sorts them so the Kernel 
   boots everything in the exact perfect order without human intervention.
"""

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
        # RLock allows the same thread to acquire the lock multiple times without deadlocking.
        self._lock = threading.RLock()
        self._runtimes: Dict[str, RuntimeInterface] = {}

    def register(self, runtime: RuntimeInterface) -> None:
        """
        Register a new runtime plugin.
        Raises ValueError if a plugin with the same name already exists.
        """
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
        """Remove a runtime from the registry (e.g., if it crashes irrecoverably)."""
        with self._lock:
            if name in self._runtimes:
                del self._runtimes[name]
                logger.info(f"Unregistered runtime: {name}")

    def list_all(self) -> List[RuntimeInterface]:
        """Return a list of all currently registered runtimes."""
        with self._lock:
            return list(self._runtimes.values())

    def get_boot_order(self) -> List[RuntimeInterface]:
        """
        Sort runtimes based on their declared dependencies (Topological Sort).
        
        WHY DO WE NEED THIS?
        If 'Storage' depends on 'Memory', we must boot 'Memory' first. 
        This graph traversal algorithm guarantees the boot sequence is flawless 
        and throws a clear error if two plugins depend on each other (Circular Dependency).
        """
        with self._lock:
            visited = set()
            temp_marks = set()
            order = []

            def visit(name: str):
                if name in temp_marks:
                    # If we see the same node while exploring its own path, it's a loop.
                    raise RuntimeError(f"Circular dependency detected involving runtime: {name}")
                if name not in visited:
                    temp_marks.add(name)
                    plugin = self._runtimes.get(name)
                    if plugin:
                        # Recursively visit all dependencies first
                        for dep in plugin.metadata().dependencies:
                            visit(dep)
                        # Once all dependencies are sorted, we can safely append this plugin
                        order.append(plugin)
                    temp_marks.remove(name)
                    visited.add(name)

            for name in self._runtimes:
                if name not in visited:
                    visit(name)
            
            return order
