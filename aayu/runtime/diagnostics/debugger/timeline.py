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
