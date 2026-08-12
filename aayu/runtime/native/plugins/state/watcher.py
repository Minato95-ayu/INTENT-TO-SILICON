import threading
from typing import Dict, Set

class StateWatcher:
    """
    Manages active subscriptions for deeply nested paths in the State Runtime.
    """
    def __init__(self):
        self._lock = threading.RLock()
        self._active_watches: Set[str] = set()

    def add_watch(self, path: str) -> None:
        with self._lock:
            self._active_watches.add(path)

    def remove_watch(self, path: str) -> None:
        with self._lock:
            if path in self._active_watches:
                self._active_watches.remove(path)

    def get_triggered_watches(self, mutated_path: str) -> Set[str]:
        """
        Determines which watched paths should be triggered when a path is mutated.
        If 'user' is mutated, 'user.address.city' must trigger.
        If 'user.address.city' is mutated, 'user' must trigger.
        """
        triggered = set()
        with self._lock:
            for watched in self._active_watches:
                # 1. Exact match (e.g. mutate 'app.counter', watch 'app.counter')
                if watched == mutated_path:
                    triggered.add(watched)
                # 2. Parent mutated (e.g. mutate 'user', watch 'user.name')
                elif watched.startswith(mutated_path + "."):
                    triggered.add(watched)
                # 3. Child mutated (e.g. mutate 'user.name', watch 'user')
                elif mutated_path.startswith(watched + "."):
                    triggered.add(watched)
        return triggered
