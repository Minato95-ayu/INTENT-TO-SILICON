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

from runtime.renderers.base import RendererInterface
from runtime.ui.display_list import DisplayList
from runtime.events.queue import EventQueue

class ConsoleRenderer(RendererInterface):
    def __init__(self, event_queue: EventQueue):
        super().__init__(event_queue)
        
    def initialize(self):
        pass
        
    def render(self, display_list: DisplayList):
        if not display_list.commands:
            return
        print("=== Console Display List ===")
        for cmd in display_list.commands:
            print(f"- {cmd}")
        print("============================")
        
    def process_events(self):
        pass
        
    def present(self):
        pass
        
    def shutdown(self):
        pass
