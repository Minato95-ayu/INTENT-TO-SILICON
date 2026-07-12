import time
import uuid
import threading
import queue
import logging
from typing import Any, Dict, Callable
from concurrent.futures import ThreadPoolExecutor
from runtime.kernel.interface import RuntimeInterface, RuntimeMetadata, DispatchResult, EventPriority

logger = logging.getLogger("aayu.kernel.scheduler")

class SchedulerRuntime(RuntimeInterface):
    """
    AAYU OS - Scheduler Runtime Plugin.
    Provides OS-level task execution, delayed timers, and concurrency.
    """
    def __init__(self, max_workers: int = 10):
        self._max_workers = max_workers
        self._queue = queue.PriorityQueue()
        self._executor = None
        self._running = False
        self._paused = False
        self._timers: Dict[str, threading.Timer] = {}
        self._lock = threading.RLock()
        self.kernel = None

        self._priority_map = {
            EventPriority.HIGH: 0,
            EventPriority.NORMAL: 1,
            EventPriority.LOW: 2
        }

    def metadata(self) -> RuntimeMetadata:
        return RuntimeMetadata(
            name="scheduler",
            version="1.0",
            dependencies=[],
            author="AAYU Core",
            priority=5  # High priority to boot early
        )

    def initialize(self, kernel) -> None:
        self.kernel = kernel

    def boot(self) -> None:
        self._executor = ThreadPoolExecutor(max_workers=self._max_workers, thread_name_prefix="aayu-worker")
        self._running = True
        
        # Start a single dispatcher thread that pulls from PriorityQueue and pushes to ThreadPoolExecutor
        self._dispatcher_thread = threading.Thread(target=self._dispatcher_loop, name="aayu-scheduler", daemon=True)
        self._dispatcher_thread.start()
        logger.info(f"Scheduler Runtime booted ({self._max_workers} workers)")

    def _dispatcher_loop(self):
        while self._running:
            try:
                # Block for a short time to allow checking _running flag
                item = self._queue.get(timeout=0.1)
                
                # Wait if paused
                while self._paused and self._running:
                    time.sleep(0.01)
                    
                if not self._running:
                    break
                    
                # Item is (priority, counter, task_id, task)
                _, _, task_id, task = item
                self._executor.submit(self._execute_task, task_id, task)
                self._queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Scheduler dispatcher error: {e}", exc_info=True)

    def _execute_task(self, task_id: str, task: Callable):
        try:
            task()
        except Exception as e:
            logger.error(f"Scheduler worker error on task {task_id}: {e}", exc_info=True)

    def start(self) -> None:
        pass

    def pause(self) -> None:
        self._paused = True

    def resume(self) -> None:
        self._paused = False

    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        start_ms = time.time()
        try:
            if action == "schedule":
                task = payload["task"]
                priority = payload.get("priority", EventPriority.NORMAL)
                task_id = payload.get("task_id", str(uuid.uuid4()))
                
                prio_num = self._priority_map.get(priority, 1)
                # We use time.time() as a secondary sort key (counter) so tasks with same priority are FIFO
                self._queue.put((prio_num, time.time(), task_id, task))
                
                return DispatchResult(success=True, data={"task_id": task_id}, time=time.time() - start_ms)

            elif action == "schedule_after":
                task = payload["task"]
                delay_ms = payload["delay_ms"]
                task_id = payload.get("task_id", str(uuid.uuid4()))
                priority = payload.get("priority", EventPriority.NORMAL)
                
                def wrapper():
                    with self._lock:
                        if task_id in self._timers:
                            del self._timers[task_id]
                    # Put back in the priority queue now that delay has passed
                    self.handle("schedule", {"task": task, "task_id": task_id, "priority": priority})

                timer = threading.Timer(delay_ms / 1000.0, wrapper)
                with self._lock:
                    self._timers[task_id] = timer
                timer.start()
                
                return DispatchResult(success=True, data={"task_id": task_id}, time=time.time() - start_ms)

            elif action == "cancel":
                task_id = payload["task_id"]
                with self._lock:
                    if task_id in self._timers:
                        self._timers[task_id].cancel()
                        del self._timers[task_id]
                        return DispatchResult(success=True, time=time.time() - start_ms)
                
                # Removing from a PriorityQueue directly isn't easy in Python, 
                # but cancellation for queue items could be handled via a cancelled_set.
                # For Phase 2, timer cancellation is the primary requirement.
                return DispatchResult(success=True, metadata={"note": "only timers strictly cancellable"}, time=time.time() - start_ms)
                
            elif action == "pause":
                self.pause()
                return DispatchResult(success=True, time=time.time() - start_ms)
                
            elif action == "resume":
                self.resume()
                return DispatchResult(success=True, time=time.time() - start_ms)

            else:
                raise ValueError(f"Unknown Scheduler action: {action}")

        except Exception as e:
            return DispatchResult(success=False, error=str(e), time=time.time() - start_ms)

    def stop(self) -> None:
        self._running = False
        with self._lock:
            for timer in self._timers.values():
                timer.cancel()
            self._timers.clear()

    def shutdown(self) -> None:
        if self._executor:
            self._executor.shutdown(wait=False)

    def health(self) -> dict:
        return {"status": "healthy"}

    def capabilities(self) -> dict:
        return {"actions": ["schedule", "schedule_after", "cancel", "pause", "resume"]}
    
    def diagnostics(self) -> dict:
        return {
            "queue_size": self._queue.qsize(),
            "pending_timers": len(self._timers),
            "paused": self._paused
        }
