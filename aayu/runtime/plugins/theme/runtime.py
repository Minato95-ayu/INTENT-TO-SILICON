import time
import logging
from typing import Any, Dict
from aayu.runtime.kernel.interface import RuntimeInterface, RuntimeMetadata, DispatchResult, EventPriority

logger = logging.getLogger("aayu.kernel.theme")

class ThemeRuntime(RuntimeInterface):
    """
    AAYU OS - Theme Runtime Plugin.
    Manages colors, typography, and spacing for the UI.
    """
    def __init__(self):
        self.kernel = None
        self._mode = "light"
        
        self._colors = {
            "light": {
                "primary": "#007BFF",
                "background": "#FFFFFF",
                "surface": "#F8F9FA",
                "text": "#212529",
                "border": "#DEE2E6",
                "error": "#DC3545"
            },
            "dark": {
                "primary": "#0D6EFD",
                "background": "#121212",
                "surface": "#1E1E1E",
                "text": "#E0E0E0",
                "border": "#333333",
                "error": "#CF6679"
            }
        }
        
        self._spacing = {
            "xs": 2,
            "sm": 4,
            "md": 8,
            "lg": 16,
            "xl": 32,
            "xxl": 64
        }
        
        self._typography = {
            "h1": {"font_size": 32, "weight": "bold"},
            "h2": {"font_size": 24, "weight": "bold"},
            "h3": {"font_size": 18, "weight": "bold"},
            "body": {"font_size": 14, "weight": "normal"},
            "caption": {"font_size": 12, "weight": "normal"}
        }

    def metadata(self) -> RuntimeMetadata:
        return RuntimeMetadata(
            name="theme",
            version="1.0",
            dependencies=[],
            author="AAYU Core",
            priority=20
        )

    def initialize(self, kernel) -> None:
        self.kernel = kernel

    def boot(self) -> None:
        logger.info(f"Theme Runtime booted (Mode: {self._mode})")

    def start(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        start_ms = time.time()
        try:
            if action == "get_mode":
                return DispatchResult(success=True, data={"mode": self._mode}, time=time.time() - start_ms)
                
            elif action == "set_mode":
                new_mode = payload.get("mode", "light")
                if new_mode in ["light", "dark"]:
                    self._mode = new_mode
                    self.kernel.bus.publish("theme.mode_changed", {"mode": self._mode}, priority=EventPriority.NORMAL, source="theme")
                return DispatchResult(success=True, time=time.time() - start_ms)
                
            elif action == "get_colors":
                return DispatchResult(success=True, data={"colors": self._colors[self._mode]}, time=time.time() - start_ms)
                
            elif action == "get_spacing":
                return DispatchResult(success=True, data={"spacing": self._spacing}, time=time.time() - start_ms)
                
            elif action == "get_typography":
                return DispatchResult(success=True, data={"typography": self._typography}, time=time.time() - start_ms)

            else:
                raise ValueError(f"Unknown Theme action: {action}")

        except Exception as e:
            return DispatchResult(success=False, error=str(e), time=time.time() - start_ms)

    def stop(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> dict:
        return {"status": "healthy"}

    def capabilities(self) -> dict:
        return {"actions": ["get_mode", "set_mode", "get_colors", "get_spacing", "get_typography"]}
    
    def diagnostics(self) -> dict:
        return {"mode": self._mode}
