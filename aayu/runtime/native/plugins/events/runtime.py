import time
import logging
from typing import Any, Dict
from aayu.runtime.kernel.interface import RuntimeInterface, RuntimeMetadata, DispatchResult, EventPriority

logger = logging.getLogger("aayu.kernel.events")

class EventRuntime(RuntimeInterface):
    """
    AAYU OS - Event Runtime Plugin.
    Bridges hardware/external I/O into the AAYU OS EventBus.
    """
    def __init__(self):
        self.kernel = None

    def metadata(self) -> RuntimeMetadata:
        return RuntimeMetadata(
            name="events",
            version="1.0",
            dependencies=[],
            author="AAYU Core",
            priority=10
        )

    def initialize(self, kernel) -> None:
        self.kernel = kernel

    def boot(self) -> None:
        logger.info("Event Runtime booted")

    def start(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        start_ms = time.time()
        try:
            if action == "fire_mouse":
                mouse_action = payload.get("action", "move")
                topic = f"input.mouse.{mouse_action}"
                self.kernel.bus.publish(topic, payload, priority=EventPriority.HIGH, source="hardware.mouse")
                return DispatchResult(success=True, time=time.time() - start_ms)
                
            elif action == "fire_keyboard":
                key_action = payload.get("action", "down")
                topic = f"input.keyboard.{key_action}"
                self.kernel.bus.publish(topic, payload, priority=EventPriority.HIGH, source="hardware.keyboard")
                return DispatchResult(success=True, time=time.time() - start_ms)
                
            elif action == "fire_touch":
                touch_action = payload.get("action", "tap")
                topic = f"input.touch.{touch_action}"
                self.kernel.bus.publish(topic, payload, priority=EventPriority.HIGH, source="hardware.touch")
                return DispatchResult(success=True, time=time.time() - start_ms)
                
            elif action == "fire_lifecycle":
                lifecycle_action = payload.get("action", "focus")
                topic = f"lifecycle.{lifecycle_action}"
                self.kernel.bus.publish(topic, payload, priority=EventPriority.SYSTEM, source="os.window")
                return DispatchResult(success=True, time=time.time() - start_ms)

            else:
                raise ValueError(f"Unknown Event action: {action}")

        except Exception as e:
            return DispatchResult(success=False, error=str(e), time=time.time() - start_ms)

    def stop(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> dict:
        return {"status": "healthy"}

    def capabilities(self) -> dict:
        return {"actions": ["fire_mouse", "fire_keyboard", "fire_touch", "fire_lifecycle"]}
    
    def diagnostics(self) -> dict:
        return {}
