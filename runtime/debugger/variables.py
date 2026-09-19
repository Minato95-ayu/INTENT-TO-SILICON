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

class VariableInspector:
    """Inspects variables safely from the VMSnapshot."""
    
    def __init__(self, snapshot):
        self.snapshot = snapshot
        
    def get_locals(self, frame_index: int = -1):
        if not self.snapshot.call_stack:
            return {}
        try:
            return self.snapshot.call_stack[frame_index]["locals"]
        except IndexError:
            return {}
            
    def get_globals(self):
        # Stub: Return global variables / State Runtime
        return {}
