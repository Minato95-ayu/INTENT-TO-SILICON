from abc import ABC, abstractmethod
from typing import Any

# Note: We will import MachineLIRModule once it is created in Phase 16.1.
# For now, it will typecheck as Any.

class BackendArtifact(ABC):
    """
    Abstract base class for all artifacts produced by a backend.
    """
    @abstractmethod
    def generate(self) -> bytes:
        """Serializes the artifact to bytes."""
        pass

class Backend(ABC):
    """
    Unified interface for all AAYU Code Generators.
    Every backend (Bytecode, LLVM, Native, WASM) must implement `lower()`.
    The input is ALWAYS a MachineLIRModule.
    """
    @abstractmethod
    def lower(self, module: Any) -> BackendArtifact:
        """
        Lowers the target-agnostic MachineLIR module into a target-specific BackendArtifact.
        """
        pass
