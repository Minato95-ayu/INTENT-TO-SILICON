import logging
from typing import List
from .interface import NativeAdapter
from ..commands import RenderCommand

logger = logging.getLogger("aayu.adapter.terminal")

class TerminalAdapter(NativeAdapter):
    """
    Mock Terminal adapter for Phase 2.
    Logs render commands for validation instead of drawing pixels.
    """
    def __init__(self):
        self.rendered_commands = []
        
    def initialize(self):
        logger.info("Terminal Adapter initialized")
        
    def render_batch(self, commands: List[RenderCommand]):
        logger.info(f"Received batch of {len(commands)} commands")
        for cmd in commands:
            self.rendered_commands.append(cmd)
            # Example: "CREATE [btn1] -> {'type': 'Button', ...}"
            logger.debug(f"{cmd.type} [{cmd.node_id}] -> {cmd.payload}")
            
    def shutdown(self):
        logger.info("Terminal Adapter shutting down")
