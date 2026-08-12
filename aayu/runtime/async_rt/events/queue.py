import queue
from typing import Any, Dict, Optional
from dataclasses import dataclass

class Event:
    pass

@dataclass
class MouseClick(Event):
    x: float
    y: float
    button: int # 1 = left, 2 = middle, 3 = right

@dataclass
class MouseMove(Event):
    x: float
    y: float

@dataclass
class MouseDown(Event):
    x: float
    y: float
    button: int

@dataclass
class MouseUp(Event):
    x: float
    y: float
    button: int

@dataclass
class KeyPress(Event):
    key: str
    code: int

@dataclass
class KeyRelease(Event):
    key: str
    code: int

@dataclass
class Scroll(Event):
    dx: float
    dy: float

@dataclass
class Resize(Event):
    width: float
    height: float

@dataclass
class Focus(Event):
    pass

@dataclass
class Blur(Event):
    pass

class EventQueue:
    def __init__(self):
        self._queue = queue.Queue()
        
    def push(self, event: Event):
        self._queue.put(event)
        
    def pop(self, block: bool = False, timeout: Optional[float] = None) -> Optional[Event]:
        try:
            return self._queue.get(block=block, timeout=timeout)
        except queue.Empty:
            return None
            
    def has_events(self) -> bool:
        return not self._queue.empty()

@dataclass
class ActionEvent(Event):
    action_name: str

@dataclass
class InputEvent(Event):
    target_state: str
    value: str

