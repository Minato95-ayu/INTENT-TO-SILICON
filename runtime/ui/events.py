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

class EventDispatcher:
    def __init__(self, vm):
        self.vm = vm
        self.on_state_changed = None
        
    def dispatch(self, action_name: str):
        print(f"[EventDispatcher] Dispatching action: {action_name}")
        self.vm.call_action_by_name(action_name)
        
        # After action completes, the state is updated.
        # Trigger a re-render!
        if self.on_state_changed:
            self.on_state_changed()
