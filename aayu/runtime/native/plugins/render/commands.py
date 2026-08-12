from typing import Any, Dict

class RenderCommand:
    """Atomic rendering command."""
    def __init__(self, cmd_type: str, node_id: str, payload: Dict[str, Any] = None):
        self.type = cmd_type
        self.node_id = node_id
        self.payload = payload or {}

# Command Types
CMD_CREATE = "CREATE"
CMD_REMOVE = "REMOVE"
CMD_MOVE = "MOVE"
CMD_UPDATE_PROPS = "UPDATE_PROPS"
CMD_UPDATE_LAYOUT = "UPDATE_LAYOUT"
CMD_SHOW = "SHOW"
CMD_HIDE = "HIDE"
