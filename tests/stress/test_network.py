import unittest
import time
from unittest.mock import patch
from aayu.runtime.kernel.core import RuntimeKernel
from aayu.runtime.plugins.network.runtime import NetworkRuntime

class TestNetworkStress(unittest.TestCase):
    def setUp(self):
        self.kernel = RuntimeKernel()
        self.network = NetworkRuntime()
        self.network.boot()
        self.kernel.registry.register(self.network)

    @patch('urllib.request.urlopen')
    def test_10k_requests(self, mock_urlopen):
        """Stress test handling 10,000 concurrent-ish API requests."""
        # Setup mock response
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.status = 200
        mock_response.headers = {}
        mock_response.read.return_value = b'{"success": true}'
        
        start_time = time.time()
        
        success_count = 0
        for i in range(10_000):
            res = self.kernel.dispatch("network", "request", {
                "request": {
                    "method": "GET",
                    "url": f"http://localhost:8080/api/mock/{i}"
                }
            })
            if res.success:
                success_count += 1
                
        duration = time.time() - start_time
        self.assertEqual(success_count, 10_000)
        self.assertTrue(duration < 5.0, f"10k network dispatches took too long: {duration}s")

if __name__ == '__main__':
    unittest.main()
