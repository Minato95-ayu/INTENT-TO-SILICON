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

"""
Event Handlers Registration

Register all workflow event handlers here.
Example:
    from event_bus import event_bus, Event
    
    def send_welcome_email(event: Event):
        pass
        
    event_bus.subscribe('patient.created', send_welcome_email)
"""
from event_bus import event_bus, Event
from logger import get_logger

logger = get_logger(__name__)
