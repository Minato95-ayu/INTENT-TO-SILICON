"""
AAYU Operating System - Runtime Interface Contract
--------------------------------------------------
File: runtime/kernel/interface.py

WHY DOES THIS FILE EXIST?
AAYU is designed as an Application Operating System, not just a script runner. 
Future versions of AAYU might have 20+ different runtimes (UI, Web, Storage, AI, etc.).
If the Kernel had to hardcode rules for how to start/stop every single runtime, 
the codebase would become a massive, unmaintainable mess of IF/ELSE statements.

WHAT DOES THIS FILE DO?
This file defines the strict "Contract" (RuntimeInterface). 
Any plugin (Storage, State, UI) that wants to run inside AAYU MUST implement these methods. 
By forcing this rule, the Kernel can blindly call `plugin.boot()` or `plugin.shutdown()` 
without needing to know what the plugin actually does. This is the foundation of 
our "Zero Circular Dependency" rule.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
import time

class RuntimeMetadata:
    """
    Holds metadata about a plugin before it is booted.
    WHY? The Kernel needs to know a plugin's dependencies *before* booting it 
    so it can calculate the correct topological boot order.
    """
    def __init__(self, name: str, version: str, dependencies: List[str], author: str, priority: int):
        self.name = name
        self.version = version
        self.dependencies = dependencies  # List of plugin names this plugin requires to boot
        self.author = author
        self.priority = priority


class DispatchResult:
    """
    Standardized return object for all plugin executions.
    WHY? If plugins return random data types, the Kernel can't reliably handle errors. 
    This struct ensures every execution explicitly reports success or failure.
    """
    def __init__(self, success: bool, data: Any = None, error: str = None, time: float = 0.0, metadata: Dict[str, Any] = None):
        self.success = success
        self.data = data
        self.error = error
        self.time = time
        self.metadata = metadata or {}


class RuntimeInterface(ABC):
    """
    The strict lifecycle interface every AAYU Runtime Plugin must implement.
    If a plugin misses even one of these methods, Python will block it from loading.
    """

    @abstractmethod
    def metadata(self) -> RuntimeMetadata:
        """Return the plugin's metadata including dependencies for boot ordering."""
        pass

    @abstractmethod
    def initialize(self, kernel) -> None:
        """
        Called once during kernel registration.
        WHY? This is where Dependency Injection happens. The plugin gets a reference 
        to the Kernel (and its Event Bus) so it doesn't have to import it globally.
        """
        pass

    @abstractmethod
    def boot(self) -> None:
        """
        Called to allocate heavy resources (e.g., opening database connections, starting sockets).
        """
        pass

    @abstractmethod
    def start(self) -> None:
        """Called to begin listening for requests or events."""
        pass

    @abstractmethod
    def pause(self) -> None:
        """Pause execution or event listening without dropping connections."""
        pass

    @abstractmethod
    def resume(self) -> None:
        """Resume execution after a pause."""
        pass

    @abstractmethod
    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        """
        Process an action requested by the Kernel or VM.
        e.g., action="insert", payload={"table": "User", "data": {...}}
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop processing new requests gracefully."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Gracefully release all resources, flush memory, and close connections."""
        pass

    @abstractmethod
    def health(self) -> dict:
        """Return current health status for diagnostics monitoring."""
        pass

    @abstractmethod
    def capabilities(self) -> dict:
        """Return a list of actions this runtime can handle."""
        pass

    @abstractmethod
    def diagnostics(self) -> dict:
        """Return deep diagnostic metrics (CPU, Memory used by this plugin)."""
        pass
