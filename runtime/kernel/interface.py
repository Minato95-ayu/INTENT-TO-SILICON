from abc import ABC, abstractmethod
from typing import Any, Dict, List
import time

class RuntimeMetadata:
    def __init__(self, name: str, version: str, dependencies: List[str], author: str, priority: int):
        self.name = name
        self.version = version
        self.dependencies = dependencies
        self.author = author
        self.priority = priority

class DispatchResult:
    def __init__(self, success: bool, data: Any = None, error: str = None, time: float = 0.0):
        self.success = success
        self.data = data
        self.error = error
        self.time = time

class RuntimeInterface(ABC):
    """
    The strict lifecycle interface every AAYU Runtime Plugin must implement.
    """
    @abstractmethod
    def metadata(self) -> RuntimeMetadata:
        """Return the plugin's metadata including dependencies for boot ordering."""
        pass

    @abstractmethod
    def initialize(self, kernel) -> None:
        """Called once during kernel registration to inject dependencies."""
        pass

    @abstractmethod
    def boot(self) -> None:
        """Called to boot up internal subsystems."""
        pass

    @abstractmethod
    def start(self) -> None:
        """Called to begin listening for requests or events."""
        pass

    @abstractmethod
    def pause(self) -> None:
        """Pause execution or event listening."""
        pass

    @abstractmethod
    def resume(self) -> None:
        """Resume execution."""
        pass

    @abstractmethod
    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        """Process an action requested by the Kernel or VM."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop processing new requests."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Gracefully release all resources."""
        pass

    @abstractmethod
    def health(self) -> dict:
        """Return current health status (e.g. {'status': 'healthy', 'uptime': 120})."""
        pass

    @abstractmethod
    def capabilities(self) -> dict:
        """Return a list of actions this runtime can handle."""
        pass

    @abstractmethod
    def diagnostics(self) -> dict:
        """Return diagnostic metrics."""
        pass
