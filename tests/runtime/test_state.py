import unittest
import threading
from typing import Any, Dict
from runtime.kernel.interface import DispatchResult
from runtime.kernel.core import RuntimeKernel
from runtime.plugins.state.runtime import StateRuntime

class TestStateRuntime(unittest.TestCase):
    def setUp(self):
        self.kernel = RuntimeKernel()
        self.state_plugin = StateRuntime()
        self.kernel.registry.register(self.state_plugin)
        self.kernel.boot()

    def tearDown(self):
        self.kernel.shutdown()

    def test_create_and_get(self):
        # Create a nested object
        initial_data = {
            "counter": 0,
            "user": {
                "name": "Ayush",
                "age": 20
            }
        }
        res_create = self.kernel.dispatch("state", "create", {"path": "app", "value": initial_data})
        self.assertTrue(res_create.success)
        
        # Get root
        res_get = self.kernel.dispatch("state", "get", {"path": "app"})
        self.assertTrue(res_get.success)
        self.assertEqual(res_get.data["counter"], 0)
        
        # Get deep path
        res_get_deep = self.kernel.dispatch("state", "get", {"path": "app.user.name"})
        self.assertTrue(res_get_deep.success)
        self.assertEqual(res_get_deep.data, "Ayush")

    def test_update_deep_path(self):
        initial_data = {"user": {"name": "Ayush", "address": {"city": "Delhi"}}}
        self.kernel.dispatch("state", "create", {"path": "app", "value": initial_data})
        
        res_update = self.kernel.dispatch("state", "set", {"path": "app.user.address.city", "value": "Mumbai"})
        self.assertTrue(res_update.success)
        
        res_get = self.kernel.dispatch("state", "get", {"path": "app.user.address.city"})
        self.assertEqual(res_get.data, "Mumbai")

    def test_delete(self):
        self.kernel.dispatch("state", "create", {"path": "temp", "value": "test"})
        res_del = self.kernel.dispatch("state", "remove", {"path": "temp"})
        self.assertTrue(res_del.success)
        
        res_get = self.kernel.dispatch("state", "get", {"path": "temp"})
        self.assertFalse(res_get.success)  # Should fail to get removed path

    def test_watchers_and_events(self):
        events_received = []
        def on_update(event):
            events_received.append(event.payload)
            
        self.kernel.bus.subscribe("state.updated", on_update)
        
        self.kernel.dispatch("state", "create", {"path": "app", "value": {"counter": 0}})
        self.kernel.dispatch("state", "watch", {"path": "app.counter"})
        
        self.kernel.dispatch("state", "set", {"path": "app.counter", "value": 1})
        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0]["path"], "app.counter")
        self.assertEqual(events_received[0]["value"], 1)

    def test_snapshot_and_restore(self):
        self.kernel.dispatch("state", "create", {"path": "app", "value": {"version": 1}})
        
        # Take snapshot
        res_snap = self.kernel.dispatch("state", "snapshot", {})
        self.assertTrue(res_snap.success)
        snap_id = res_snap.data["snapshot_id"]
        
        # Mutate
        self.kernel.dispatch("state", "set", {"path": "app.version", "value": 2})
        self.assertEqual(self.kernel.dispatch("state", "get", {"path": "app.version"}).data, 2)
        
        # Restore
        res_restore = self.kernel.dispatch("state", "restore", {"snapshot_id": snap_id})
        self.assertTrue(res_restore.success)
        self.assertEqual(self.kernel.dispatch("state", "get", {"path": "app.version"}).data, 1)

    def test_concurrent_mutations(self):
        self.kernel.dispatch("state", "create", {"path": "app", "value": {"counter": 0}})
        
        def worker():
            for _ in range(100):
                # We need an atomic increment ideally, but for now we simulate simple set
                val = self.kernel.dispatch("state", "get", {"path": "app.counter"}).data
                self.kernel.dispatch("state", "set", {"path": "app.counter", "value": val + 1})
                
        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads: t.start()
        for t in threads: t.join()
        
        # Since standard set isn't an atomic CAS (Compare-And-Swap), we just ensure the state engine didn't crash.
        # It's at least > 0.
        res = self.kernel.dispatch("state", "get", {"path": "app.counter"})
        self.assertTrue(res.success)
        self.assertGreater(res.data, 0)

if __name__ == '__main__':
    unittest.main()
