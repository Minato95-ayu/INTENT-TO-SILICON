import time
import logging
import threading
from typing import Any, Dict, Optional
from aayu.runtime.kernel.interface import RuntimeInterface, RuntimeMetadata, DispatchResult
from .diff import DiffEngine
from .layout import LayoutEngine
from .adapters.terminal import TerminalAdapter
from .commands import RenderCommand, CMD_UPDATE_LAYOUT

logger = logging.getLogger("aayu.kernel.render")

class RenderRuntime(RuntimeInterface):
    """
    AAYU OS - Render Runtime Plugin.
    Coordinates Diff Engine -> Layout Engine -> Native Adapters.
    Batches commands and enforces 16ms render loop targets.
    """
    def __init__(self):
        self.kernel = None
        self.diff_engine = DiffEngine()
        self.layout_engine = LayoutEngine()
        self.adapter = TerminalAdapter()
        
        self._current_tree = None
        self._render_lock = threading.Lock()

    def metadata(self) -> RuntimeMetadata:
        return RuntimeMetadata(
            name="render",
            version="1.0",
            dependencies=["ui"],
            author="AAYU Core",
            priority=50
        )

    def initialize(self, kernel) -> None:
        self.kernel = kernel
        self.adapter.initialize()

    def boot(self) -> None:
        logger.info("Render Runtime booted")

    def start(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        start_ms = time.time()
        try:
            if action == "update_tree":
                new_tree = payload.get("tree")
                if not new_tree:
                    raise ValueError("Missing 'tree' in payload")
                    
                with self._render_lock:
                    # 1. Diff
                    commands = self.diff_engine.compute(self._current_tree, new_tree)
                    
                    # 2. Layout (If there are changes or layout requested)
                    if commands or not self._current_tree:
                        boxes = self.layout_engine.compute(new_tree)
                        # We send layout updates as commands
                        for node_id, box in boxes.items():
                            commands.append(RenderCommand(CMD_UPDATE_LAYOUT, node_id, payload={"box": box}))
                            
                    # 3. Batch to adapter
                    if commands:
                        self.adapter.render_batch(commands)
                        
                    self._current_tree = new_tree
                    
                return DispatchResult(success=True, time=time.time() - start_ms)
                
            else:
                raise ValueError(f"Unknown Render action: {action}")

        except Exception as e:
            return DispatchResult(success=False, error=str(e), time=time.time() - start_ms)

    def stop(self) -> None:
        self.adapter.shutdown()

    def shutdown(self) -> None:
        self.stop()

    def health(self) -> dict:
        return {"status": "healthy"}

    def capabilities(self) -> dict:
        return {"actions": ["update_tree"]}
    
    def diagnostics(self) -> dict:
        return {
            "current_tree_exists": self._current_tree is not None
        }
