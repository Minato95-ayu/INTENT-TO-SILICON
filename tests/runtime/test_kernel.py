import unittest
import threading
from typing import Any, Dict
from runtime.kernel.interface import RuntimeInterface, RuntimeMetadata, DispatchResult
from runtime.kernel.core import RuntimeKernel

class DummyPlugin(RuntimeInterface):
    def __init__(self, name: str, dependencies: list = None):
        self._name = name
        self._deps = dependencies or []
        self.initialized = False
        self.started = False
        self.stopped = False
        self.shutdown_called = False
        self.handles = []
        self.should_crash_on_handle = False
        self.should_crash_on_boot = False

    def metadata(self) -> RuntimeMetadata:
        return RuntimeMetadata(
            name=self._name,
            version="1.0",
            dependencies=self._deps,
            author="Test",
            priority=0
        )

    def initialize(self, kernel) -> None:
        if self.should_crash_on_boot:
            raise RuntimeError(f"{self._name} crash on boot")
        self.initialized = True
        self.kernel = kernel

    def boot(self) -> None:
        pass

    def start(self) -> None:
        self.started = True

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        if self.should_crash_on_handle:
            raise ValueError(f"{self._name} handle crash")
        self.handles.append((action, payload))
        return DispatchResult(success=True, data=payload, error=None, time=0.0)

    def stop(self) -> None:
        self.stopped = True

    def shutdown(self) -> None:
        self.shutdown_called = True

    def health(self) -> dict:
        return {"status": "healthy"}

    def capabilities(self) -> dict:
        return {}
    
    def diagnostics(self) -> dict:
        return {}


class TestRuntimeKernel(unittest.TestCase):
    def setUp(self):
        self.kernel = RuntimeKernel()

    def test_registration_and_missing(self):
        plugin = DummyPlugin("storage")
        self.kernel.registry.register(plugin)
        
        # Test duplicate
        with self.assertRaises(ValueError):
            self.kernel.registry.register(plugin)

        # Test missing
        p = self.kernel.registry.get("missing")
        self.assertIsNone(p)

    def test_boot_sequence_and_dependencies(self):
        # Register in random order, Kernel should sort via topological sort
        self.kernel.registry.register(DummyPlugin("ui", dependencies=["state"]))
        self.kernel.registry.register(DummyPlugin("state", dependencies=["storage"]))
        self.kernel.registry.register(DummyPlugin("storage", dependencies=[]))
        
        self.kernel.boot()
        
        storage = self.kernel.registry.get("storage")
        state = self.kernel.registry.get("state")
        ui = self.kernel.registry.get("ui")
        
        self.assertTrue(storage.initialized and storage.started)
        self.assertTrue(state.initialized and state.started)
        self.assertTrue(ui.initialized and ui.started)
        
        self.kernel.shutdown()
        self.assertTrue(ui.stopped and ui.shutdown_called)

    def test_dispatch_and_plugin_isolation(self):
        p1 = DummyPlugin("db")
        p2 = DummyPlugin("crashy")
        p2.should_crash_on_handle = True
        
        self.kernel.registry.register(p1)
        self.kernel.registry.register(p2)
        self.kernel.boot()
        
        res1 = self.kernel.dispatch("db", "insert", {"id": 1})
        self.assertTrue(res1.success)
        self.assertEqual(res1.data, {"id": 1})
        
        # Isolation: crashy plugin fails but returns error result without crashing OS
        res2 = self.kernel.dispatch("crashy", "run", {})
        self.assertFalse(res2.success)
        self.assertIsNotNone(res2.error)
        self.assertIn("crash", res2.error)

    def test_event_bus_thread_safety(self):
        events_received = []
        lock = threading.Lock()
        
        def callback(payload):
            with lock:
                events_received.append(payload)
                
        self.kernel.bus.subscribe("test.event", callback)
        
        def worker():
            for i in range(1000):
                self.kernel.bus.publish("test.event", i)
                
        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads: t.start()
        for t in threads: t.join()
        
        self.assertEqual(len(events_received), 10000)

    def test_stress_registration_and_memory(self):
        # Simulate boot and shutdown cycles to test memory leaks/state resets
        for i in range(100):
            kernel = RuntimeKernel()
            p = DummyPlugin(f"p_{i}")
            kernel.registry.register(p)
            kernel.boot()
            kernel.shutdown()
            self.assertTrue(p.stopped)
            self.assertTrue(p.shutdown_called)

if __name__ == '__main__':
    unittest.main()
