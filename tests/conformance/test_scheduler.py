import unittest
import threading
import time
from typing import Any, Dict
from aayu.runtime.kernel.interface import DispatchResult, EventPriority
from aayu.runtime.kernel.core import RuntimeKernel
from aayu.runtime.plugins.scheduler.runtime import SchedulerRuntime

class TestSchedulerRuntime(unittest.TestCase):
    def setUp(self):
        self.kernel = RuntimeKernel()
        self.scheduler = SchedulerRuntime()
        self.kernel.registry.register(self.scheduler)
        self.kernel.boot()
        
    def tearDown(self):
        self.kernel.shutdown()

    def test_queue_ordering(self):
        results = []
        lock = threading.Lock()
        
        def task_low():
            with lock:
                results.append("LOW")
                
        def task_high():
            with lock:
                results.append("HIGH")
                
        def task_normal():
            with lock:
                results.append("NORMAL")
        
        # Pause the scheduler so tasks are queued without executing immediately
        self.kernel.dispatch("scheduler", "pause", {})
        
        # Schedule in reverse priority order
        self.kernel.dispatch("scheduler", "schedule", {"task": task_low, "priority": EventPriority.LOW})
        self.kernel.dispatch("scheduler", "schedule", {"task": task_normal, "priority": EventPriority.NORMAL})
        self.kernel.dispatch("scheduler", "schedule", {"task": task_high, "priority": EventPriority.HIGH})
        
        # Resume and wait briefly
        self.kernel.dispatch("scheduler", "resume", {})
        time.sleep(0.1) # Wait for workers to process
        
        # The executor should have picked HIGH first, then NORMAL, then LOW
        with lock:
            self.assertEqual(results, ["HIGH", "NORMAL", "LOW"])

    def test_delayed_execution(self):
        results = []
        lock = threading.Lock()
        
        def delayed_task():
            with lock:
                results.append(time.time())
                
        start_time = time.time()
        self.kernel.dispatch("scheduler", "schedule_after", {"task": delayed_task, "delay_ms": 200})
        
        # Ensure it hasn't run yet
        time.sleep(0.05)
        with lock:
            self.assertEqual(len(results), 0)
            
        # Ensure it runs after ~200ms
        time.sleep(0.3)
        with lock:
            self.assertEqual(len(results), 1)
            # Drift should be acceptable (<50ms for tests usually)
            drift = results[0] - start_time - 0.2
            self.assertTrue(-0.05 < drift < 0.2, f"Timer drift too large: {drift}")

    def test_cancellation(self):
        results = []
        
        def task():
            results.append("RAN")
            
        res = self.kernel.dispatch("scheduler", "schedule_after", {"task": task, "delay_ms": 100})
        task_id = res.data["task_id"]
        
        # Cancel immediately
        cancel_res = self.kernel.dispatch("scheduler", "cancel", {"task_id": task_id})
        self.assertTrue(cancel_res.success)
        
        time.sleep(0.2)
        self.assertEqual(len(results), 0)

    def test_concurrent_scheduling(self):
        results = []
        lock = threading.Lock()
        
        def worker_task(i):
            with lock:
                results.append(i)
                
        def submit_tasks():
            for i in range(100):
                self.kernel.dispatch("scheduler", "schedule", {"task": lambda i=i: worker_task(i)})
                
        threads = [threading.Thread(target=submit_tasks) for _ in range(10)]
        for t in threads: t.start()
        for t in threads: t.join()
        
        # Allow time for scheduler workers to process 1000 tasks
        time.sleep(0.5)
        with lock:
            self.assertEqual(len(results), 1000)

    def test_shutdown_cleanup(self):
        # Schedule a very long delayed task
        self.kernel.dispatch("scheduler", "schedule_after", {"task": lambda: None, "delay_ms": 10000})
        
        # Shutdown kernel
        self.kernel.shutdown()
        
        # Internally it should clean up timers
        diag = self.scheduler.diagnostics()
        self.assertEqual(diag.get("pending_timers", 0), 0)
        self.assertEqual(diag.get("queue_size", 0), 0)

if __name__ == '__main__':
    unittest.main()
