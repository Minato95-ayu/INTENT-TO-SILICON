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

from typing import List
from ..commands import RenderCommand

class NativeAdapter:
    """Base interface for Platform Render Adapters."""
    def initialize(self):
        pass
        
    def render_batch(self, commands: List[RenderCommand]):
        raise NotImplementedError("Adapters must implement render_batch")
        
    def shutdown(self):
        pass
