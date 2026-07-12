import time
import logging
from typing import Any, Dict
from runtime.kernel.interface import RuntimeInterface, RuntimeMetadata, DispatchResult
from .widgets import WIDGET_REGISTRY, UIElement

logger = logging.getLogger("aayu.kernel.ui")

class UIRuntime(RuntimeInterface):
    """
    AAYU OS - UI Runtime Plugin.
    Generates logical Widget trees from AST. Never draws pixels.
    """
    def __init__(self):
        self.kernel = None

    def metadata(self) -> RuntimeMetadata:
        return RuntimeMetadata(
            name="ui",
            version="1.0",
            dependencies=[],
            author="AAYU Core",
            priority=40
        )

    def initialize(self, kernel) -> None:
        self.kernel = kernel

    def boot(self) -> None:
        logger.info("UI Runtime booted")

    def start(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass
        
    def _build_node(self, node_ast: Dict[str, Any]) -> UIElement:
        w_type = node_ast.get("type")
        if not w_type or w_type not in WIDGET_REGISTRY:
            raise ValueError(f"Unknown widget type: {w_type}")
            
        WidgetClass = WIDGET_REGISTRY[w_type]
        
        # If the AST dictates an ID (e.g. for reactive updates), use it. Else generate.
        element_id = node_ast.get("id")
        props = node_ast.get("props", {})
        
        element = WidgetClass(element_id=element_id, props=props)
        
        children_ast = node_ast.get("children", [])
        for c_ast in children_ast:
            child_element = self._build_node(c_ast)
            element.add_child(child_element)
            
        return element

    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        start_ms = time.time()
        try:
            if action == "build":
                ast = payload.get("ast")
                if not ast:
                    raise ValueError("Missing 'ast' in payload")
                    
                tree = self._build_node(ast)
                return DispatchResult(success=True, data={"tree": tree}, time=time.time() - start_ms)
                
            elif action == "build_mini_tree":
                # For reactive dependency graph updates. We only build the affected sub-tree.
                ast = payload.get("ast")
                if not ast:
                    raise ValueError("Missing 'ast' in payload")
                    
                mini_tree = self._build_node(ast)
                return DispatchResult(success=True, data={"tree": mini_tree}, time=time.time() - start_ms)

            else:
                raise ValueError(f"Unknown UI action: {action}")

        except Exception as e:
            return DispatchResult(success=False, error=str(e), time=time.time() - start_ms)

    def stop(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> dict:
        return {"status": "healthy"}

    def capabilities(self) -> dict:
        return {"actions": ["build", "build_mini_tree"]}
    
    def diagnostics(self) -> dict:
        return {}
