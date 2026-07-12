import threading
import logging
from typing import Dict, List, Callable, Any

logger = logging.getLogger("aayu.kernel")

class EventBus:
    """
    Thread-safe generic Pub/Sub Event System for AAYU OS.
    """
    def __init__(self):
        self._lock = threading.RLock()
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, topic: str, callback: Callable[[Any], None]) -> None:
        """Subscribe to a specific event topic."""
        with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            if callback not in self._subscribers[topic]:
                self._subscribers[topic].append(callback)

    def unsubscribe(self, topic: str, callback: Callable[[Any], None]) -> None:
        """Unsubscribe from a specific event topic."""
        with self._lock:
            if topic in self._subscribers and callback in self._subscribers[topic]:
                self._subscribers[topic].remove(callback)

    def publish(self, topic: str, payload: Any) -> None:
        """Publish an event to all subscribers of a topic."""
        with self._lock:
            subs = list(self._subscribers.get(topic, []))
            
        for callback in subs:
            try:
                callback(payload)
            except Exception as e:
                logger.error(f"EventBus: Exception in callback for topic '{topic}': {e}", exc_info=True)
