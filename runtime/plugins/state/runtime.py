import time
import uuid
import logging
from typing import Any, Dict
from runtime.kernel.interface import RuntimeInterface, RuntimeMetadata, DispatchResult
from .store import StateStore
from .watcher import StateWatcher

logger = logging.getLogger("aayu.kernel.state")

class StateRuntime(RuntimeInterface):
    """
    AAYU OS - State Runtime Plugin.
    Manages global, reactive state for the OS.
    """
    def __init__(self):
        self.store = StateStore()
        self.watcher = StateWatcher()
        self._snapshots: Dict[str, Dict[str, Any]] = {}
        self.kernel = None

    def metadata(self) -> RuntimeMetadata:
        return RuntimeMetadata(
            name="state",
            version="1.0",
            dependencies=[],  # State depends on nothing
            author="AAYU Core",
            priority=10
        )

    def initialize(self, kernel) -> None:
        self.kernel = kernel

    def boot(self) -> None:
        pass

    def start(self) -> None:
        logger.info("State Runtime started.")

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def _publish_change(self, topic: str, path: str, value: Any = None):
        """Publish an event to the EventBus if kernel is available."""
        if self.kernel and self.kernel.bus:
            payload = {"path": path}
            if value is not None:
                payload["value"] = value
            self.kernel.bus.publish(topic, payload)

            # Trigger specific path watchers
            triggered_paths = self.watcher.get_triggered_watches(path)
            for t_path in triggered_paths:
                if t_path != path:
                    try:
                        t_val = self.store.get(t_path)
                        self.kernel.bus.publish("state.updated", {"path": t_path, "value": t_val})
                    except KeyError:
                        pass

    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        start_ms = time.time()
        
        try:
            if action == "create" or action == "set":
                path = payload["path"]
                val = payload["value"]
                self.store.set(path, val)
                
                # Determine topic based on whether it was explicitly a create or set
                topic = "state.created" if action == "create" else "state.updated"
                self._publish_change(topic, path, val)
                
                return DispatchResult(success=True, data=val, time=time.time() - start_ms)

            elif action == "get":
                path = payload["path"]
                val = self.store.get(path)
                return DispatchResult(success=True, data=val, time=time.time() - start_ms)

            elif action == "remove":
                path = payload["path"]
                self.store.remove(path)
                self._publish_change("state.deleted", path)
                return DispatchResult(success=True, time=time.time() - start_ms)

            elif action == "watch":
                path = payload["path"]
                self.watcher.add_watch(path)
                return DispatchResult(success=True, time=time.time() - start_ms)

            elif action == "unwatch":
                path = payload["path"]
                self.watcher.remove_watch(path)
                return DispatchResult(success=True, time=time.time() - start_ms)

            elif action == "snapshot":
                snap_id = str(uuid.uuid4())
                self._snapshots[snap_id] = self.store.snapshot()
                
                if self.kernel and self.kernel.bus:
                    self.kernel.bus.publish("state.snapshot", {"snapshot_id": snap_id})
                    
                return DispatchResult(success=True, data={"snapshot_id": snap_id}, time=time.time() - start_ms)

            elif action == "restore":
                snap_id = payload["snapshot_id"]
                if snap_id not in self._snapshots:
                    raise ValueError(f"Snapshot ID {snap_id} not found.")
                
                self.store.restore(self._snapshots[snap_id])
                
                if self.kernel and self.kernel.bus:
                    self.kernel.bus.publish("state.restore", {"snapshot_id": snap_id})
                    
                return DispatchResult(success=True, time=time.time() - start_ms)

            else:
                raise ValueError(f"Unknown State Runtime action: {action}")

        except Exception as e:
            return DispatchResult(success=False, error=str(e), time=time.time() - start_ms)

    def stop(self) -> None:
        pass

    def shutdown(self) -> None:
        self._snapshots.clear()
        self.store = StateStore()

    def health(self) -> dict:
        return {"status": "healthy"}

    def capabilities(self) -> dict:
        return {"actions": ["create", "set", "get", "remove", "watch", "unwatch", "snapshot", "restore"]}
    
    def diagnostics(self) -> dict:
        return {"snapshots_count": len(self._snapshots)}
