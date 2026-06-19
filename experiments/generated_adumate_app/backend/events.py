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
