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

import time

class Timeline:
    """Maintains event history for the debugger."""
    def __init__(self):
        self.events = []
        
    def record(self, event_type: str, details: str):
        self.events.append({
            "timestamp": time.time(),
            "type": event_type,
            "details": details
        })
        
    def get_history(self):
        return self.events
        
    def clear(self):
        self.events.clear()
