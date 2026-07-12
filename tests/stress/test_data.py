import unittest
import time
from runtime.kernel.core import RuntimeKernel
from runtime.plugins.storage.runtime import StorageRuntime

class TestDataStress(unittest.TestCase):
    def setUp(self):
        self.kernel = RuntimeKernel()
        self.storage = StorageRuntime(in_memory=True)
        self.storage.boot()
        self.kernel.registry.register(self.storage)

    def test_massive_dataset_simulation(self):
        """Stress test for large dataset handling via Storage Runtime."""
        start_time = time.time()
        
        self.kernel.dispatch("storage", "migrate", {
            "schema": {
                "name": "Log",
                "fields": [
                    {"name": "id", "type": "Int"},
                    {"name": "message", "type": "String"}
                ]
            }
        })
        
        batch_size = 10_000
        
        # Insert batch
        for i in range(batch_size):
            self.kernel.dispatch("storage", "insert", {
                "model": "Log",
                "data": {"id": i, "message": f"Log entry {i} "*10}
            })
            
        # Query large dataset
        res = self.kernel.dispatch("storage", "query", {
            "model": "Log",
            "filters": {}
        })
        
        duration = time.time() - start_time
        
        self.assertEqual(len(res.data), batch_size)
        self.assertTrue(duration < 15.0, f"Massive data simulation took too long: {duration}s")

if __name__ == '__main__':
    unittest.main()
