import unittest
import threading
import time
from typing import Any, Dict
from runtime.kernel.interface import DispatchResult, EventPriority
from runtime.kernel.core import RuntimeKernel
from runtime.plugins.events.runtime import EventRuntime

class TestEventRuntime(unittest.TestCase):
    def setUp(self):
        self.kernel = RuntimeKernel()
        self.event_runtime = EventRuntime()
        self.kernel.registry.register(self.event_runtime)
        self.kernel.boot()

    def tearDown(self):
        self.kernel.shutdown()

    def test_mouse_event_bridging(self):
        events_received = []
        
        def on_mouse(event):
            events_received.append(event.payload)
            
        self.kernel.bus.subscribe("input.mouse.click", on_mouse)
        
        res = self.kernel.dispatch("events", "fire_mouse", {
            "action": "click",
            "x": 100,
            "y": 200,
            "button": "left"
        })
        
        self.assertTrue(res.success)
        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0]["x"], 100)
        self.assertEqual(events_received[0]["y"], 200)

    def test_keyboard_event_bridging(self):
        events_received = []
        
        def on_key(event):
            events_received.append(event.payload)
            
        self.kernel.bus.subscribe("input.keyboard.down", on_key)
        
        res = self.kernel.dispatch("events", "fire_keyboard", {
            "action": "down",
            "key": "Enter",
            "code": 13
        })
        
        self.assertTrue(res.success)
        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0]["key"], "Enter")

    def test_high_frequency_stress(self):
        events_received = []
        lock = threading.Lock()
        
        def on_touch(event):
            with lock:
                events_received.append(event.payload)
                
        self.kernel.bus.subscribe("input.touch.move", on_touch)
        
        def simulate_touch():
            for i in range(1000):
                self.kernel.dispatch("events", "fire_touch", {
                    "action": "move",
                    "x": i,
                    "y": i
                })
                
        threads = [threading.Thread(target=simulate_touch) for _ in range(10)]
        for t in threads: t.start()
        for t in threads: t.join()
        
        self.assertEqual(len(events_received), 10000)

if __name__ == '__main__':
    unittest.main()
