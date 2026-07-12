from typing import Dict, Any, List
from runtime.base import BaseRuntime

class RuntimeManager:
    """
    Orchestrates the independent Native Runtimes (HTTP, DB, UI).
    Decouples the core VM from platform specifics.
    """
    def __init__(self, app_metadata: Dict[str, Any]):
        self.app_metadata = app_metadata
        self.active_runtimes: List[BaseRuntime] = []

    def initialize(self):
        """
        Dynamically load runtimes based on AppIR metadata.
        """
        # Load Database Runtime
        if self.app_metadata.get("data_ir", {}).get("models") or self.app_metadata.get("data_ir", {}).get("storages"):
            try:
                from runtime.database.runtime import DatabaseRuntime
                db_runtime = DatabaseRuntime(self.app_metadata)
                self.active_runtimes.append(db_runtime)
                print("[AAYU] Native Database Runtime loaded.")
            except ImportError as e:
                print(f"[AAYU] Warning: Database runtime not found. ({e})")

        # Load HTTP Runtime
        if self.app_metadata.get("api_ir", {}).get("services"):
            try:
                from runtime.http.runtime import HTTPRuntime
                http_runtime = HTTPRuntime(self.app_metadata)
                self.active_runtimes.append(http_runtime)
                print("[AAYU] Native HTTP Runtime loaded.")
            except ImportError as e:
                print(f"[AAYU] Warning: HTTP runtime not found. ({e})")

        # Load UI Runtime
        if self.app_metadata.get("ui_ir", {}).get("serve"):
            try:
                from runtime.ui.runtime import UIRuntime
                ui_runtime = UIRuntime(self.app_metadata)
                self.active_runtimes.append(ui_runtime)
                print("[AAYU] Native UI Runtime loaded.")
            except ImportError as e:
                print(f"[AAYU] Warning: UI runtime not found. ({e})")

        # Initialize all loaded runtimes
        for runtime in self.active_runtimes:
            runtime.initialize()

    def start(self):
        """
        Start all runtimes sequentially (some might block, so ideally we thread them).
        For now, we'll start them sequentially. The HTTP/UI servers are usually blocking.
        """
        import threading
        threads = []
        for runtime in self.active_runtimes:
            t = threading.Thread(target=runtime.start)
            t.daemon = False # We want the main process to wait for these
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()

    def get_runtime(self, name):
        for runtime in self.active_runtimes:
            if type(runtime).__name__ == name:
                return runtime
        return None
