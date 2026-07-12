"""
=============================================================================
FILE: event_bus.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import BackgroundTasks
import uuid
from logger import get_logger

logger = get_logger(__name__)

class Event(BaseModel):
    id: str
    name: str
    entity: str
    action: str
    payload: Dict[str, Any]
    request_id: str
    timestamp: datetime

class EventBus:
    def emit(self, background_tasks: BackgroundTasks, event: Event) -> None:
        raise NotImplementedError

    def subscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        raise NotImplementedError

class FastAPIBackgroundEventBus(EventBus):
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)
        logger.info(f'Subscribed handler {handler.__name__} to event {event_name}')

    def emit(self, background_tasks: BackgroundTasks, event: Event) -> None:
        handlers = self._subscribers.get(event.name, [])
        if not handlers:
            return
        
        for handler in handlers:
            background_tasks.add_task(self._safe_execute, handler, event)
            
    def _safe_execute(self, handler: Callable[[Event], None], event: Event) -> None:
        try:
            handler(event)
            logger.info(f'Successfully executed handler {handler.__name__} for event {event.name}', extra={'request_id': event.request_id})
        except Exception as e:
            logger.error(f'Error executing handler {handler.__name__} for event {event.name}: {str(e)}', exc_info=True, extra={'request_id': event.request_id})

# Global singleton instance
event_bus = FastAPIBackgroundEventBus()
