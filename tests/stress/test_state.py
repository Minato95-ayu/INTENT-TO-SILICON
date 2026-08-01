import unittest
import time
from aayu.runtime.kernel.core import RuntimeKernel
from aayu.runtime.plugins.state.runtime import StateRuntime

class TestStateStress(unittest.TestCase):
    def setUp(self):
        self.kernel = RuntimeKernel()
        self.state_runtime = StateRuntime()
        self.state_runtime.boot()
        self.kernel.registry.register(self.state_runtime)

    def test_100k_state_updates(self):
        """Stress test 100,000 reactive state updates."""
        start_time = time.time()
        
        # Initialize
        self.kernel.dispatch("state", "create", {"path": "counter", "value": 0})
        
        # Update 100,000 times
        for i in range(100_000):
            self.kernel.dispatch("state", "set", {"path": "counter", "value": i})
            
        duration = time.time() - start_time
        
        res = self.kernel.dispatch("state", "get", {"path": "counter"})
        self.assertEqual(res.data, 99999)
        self.assertTrue(duration < 5.0, f"100k state updates took too long: {duration}s")

if __name__ == '__main__':
    unittest.main()
