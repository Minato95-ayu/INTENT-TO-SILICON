from typing import Dict, Any

class BaseRuntime:
    """
    The base class for all AAYU Native Runtimes.
    All runtimes (HTTP, UI, Database, FileSystem) must implement this interface.
    """
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata

    def initialize(self):
        """
        Called to prepare the runtime (e.g., connect to DB, parse routes).
        """
        pass

    def start(self):
        """
        Called to start the runtime (e.g., spin up a server).
        """
        pass
