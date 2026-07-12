"""
AAYU Operating System - Event Bus
---------------------------------
File: runtime/kernel/bus.py

WHY DOES THIS FILE EXIST?
In a standard application, if the UI needs to save data, it imports the Database. 
In an Operating System architecture, this creates massive tangled dependencies. 
To keep plugins 100% isolated, we use a generic Event Bus. 
The UI publishes "state.changed", and the Storage plugin subscribes to it. 
They never know the other exists.

WHAT DOES THIS CODE DO?
It is a strictly thread-safe Publisher/Subscriber (Pub/Sub) pattern. 
It protects its internal subscriber list using `threading.RLock`, ensuring that 
events fired from background async threads do not corrupt the subscriber lists 
used by the main UI thread.
"""

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
        """
        Subscribe a callback function to a specific event topic.
        e.g., kernel.bus.subscribe("storage.inserted", my_callback)
        """
        with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            if callback not in self._subscribers[topic]:
                self._subscribers[topic].append(callback)

    def unsubscribe(self, topic: str, callback: Callable[[Any], None]) -> None:
        """
        Remove a callback from a topic. Used during plugin shutdown to prevent memory leaks.
        """
        with self._lock:
            if topic in self._subscribers and callback in self._subscribers[topic]:
                self._subscribers[topic].remove(callback)

    def publish(self, topic: str, payload: Any) -> None:
        """
        Publish an event to all subscribers of a topic.
        WHY USE try/except INSIDE THE LOOP?
        If one subscriber's callback throws a crash, we MUST catch it. If we don't, 
        the exception halts the loop, and the remaining subscribers never receive the event.
        """
        with self._lock:
            # We copy the list of subscribers to prevent a deadlock if a subscriber 
            # tries to unsubscribe *during* the execution of its callback.
            subs = list(self._subscribers.get(topic, []))
            
        for callback in subs:
            try:
                callback(payload)
            except Exception as e:
                # We log the error but swallow the exception to protect the Event Bus
                logger.error(f"EventBus: Exception in callback for topic '{topic}': {e}", exc_info=True)
