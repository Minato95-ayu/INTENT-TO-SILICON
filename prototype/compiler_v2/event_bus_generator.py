"""
Aayu Event Bus Generator

Generates the foundation for the event-driven architecture.
"""
from typing import Dict
from .schema_nodes import SchemaModel

class EventBusGenerator:
    def generate(self, schema: SchemaModel) -> Dict[str, str]:
        event_bus_code = [
            "from typing import Any, Callable, Dict, List, Optional",
            "from pydantic import BaseModel",
            "from datetime import datetime",
            "from fastapi import BackgroundTasks",
            "import uuid",
            "from logger import get_logger",
            "",
            "logger = get_logger(__name__)",
            "",
            "class Event(BaseModel):",
            "    id: str",
            "    name: str",
            "    entity: str",
            "    action: str",
            "    payload: Dict[str, Any]",
            "    request_id: str",
            "    timestamp: datetime",
            "",
            "class EventBus:",
            "    def emit(self, background_tasks: BackgroundTasks, event: Event) -> None:",
            "        raise NotImplementedError",
            "",
            "    def subscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:",
            "        raise NotImplementedError",
            "",
            "class FastAPIBackgroundEventBus(EventBus):",
            "    def __init__(self):",
            "        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}",
            "",
            "    def subscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:",
            "        if event_name not in self._subscribers:",
            "            self._subscribers[event_name] = []",
            "        self._subscribers[event_name].append(handler)",
            "        logger.info(f'Subscribed handler {handler.__name__} to event {event_name}')",
            "",
            "    def emit(self, background_tasks: BackgroundTasks, event: Event) -> None:",
            "        handlers = self._subscribers.get(event.name, [])",
            "        if not handlers:",
            "            return",
            "        ",
            "        for handler in handlers:",
            "            background_tasks.add_task(self._safe_execute, handler, event)",
            "            ",
            "    def _safe_execute(self, handler: Callable[[Event], None], event: Event) -> None:",
            "        try:",
            "            handler(event)",
            "            logger.info(f'Successfully executed handler {handler.__name__} for event {event.name}', extra={'request_id': event.request_id})",
            "        except Exception as e:",
            "            logger.error(f'Error executing handler {handler.__name__} for event {event.name}: {str(e)}', exc_info=True, extra={'request_id': event.request_id})",
            "",
            "# Global singleton instance",
            "event_bus = FastAPIBackgroundEventBus()",
            ""
        ]

        events_code = [
            "\"\"\"",
            "Event Handlers Registration",
            "",
            "Register all workflow event handlers here.",
            "Example:",
            "    from event_bus import event_bus, Event",
            "    ",
            "    def send_welcome_email(event: Event):",
            "        pass",
            "        ",
            "    event_bus.subscribe('patient.created', send_welcome_email)",
            "\"\"\"",
            "from event_bus import event_bus, Event",
            "from logger import get_logger",
            "",
            "logger = get_logger(__name__)",
            ""
        ]

        return {
            "event_bus.py": "\n".join(event_bus_code),
            "events.py": "\n".join(events_code)
        }
