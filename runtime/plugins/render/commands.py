# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

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
