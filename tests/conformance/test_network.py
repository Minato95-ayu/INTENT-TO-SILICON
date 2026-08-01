import unittest
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict
from aayu.runtime.kernel.interface import DispatchResult
from aayu.runtime.kernel.core import RuntimeKernel
from aayu.runtime.plugins.network.runtime import NetworkRuntime

# Mock Server for testing network outbound calls
class MockServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/timeout":
            time.sleep(2)
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "ok", "method": "GET"}')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {"status": "created", "method": "POST", "body": post_data.decode('utf-8')}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def log_message(self, format, *args):
        pass # Suppress logs


class TestNetworkRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start mock server
        cls.server = HTTPServer(('127.0.0.1', 9999), MockServerHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.kernel = RuntimeKernel()
        self.network = NetworkRuntime()
        self.kernel.registry.register(self.network)
        self.kernel.boot()

    def tearDown(self):
        self.kernel.shutdown()

    def test_get_request(self):
        res = self.kernel.dispatch("network", "request", {
            "request": {
                "method": "GET",
                "url": "http://127.0.0.1:9999/api",
                "headers": {},
                "body": None,
                "timeout": 5
            }
        })
        self.assertTrue(res.success)
        response = res.data["response"]
        self.assertEqual(response["status"], 200)
        self.assertEqual(json.loads(response["body"])["method"], "GET")

    def test_post_request(self):
        payload = '{"name": "aayu"}'
        res = self.kernel.dispatch("network", "request", {
            "request": {
                "method": "POST",
                "url": "http://127.0.0.1:9999/api",
                "headers": {"Content-Length": str(len(payload))},
                "body": payload,
                "timeout": 5
            }
        })
        self.assertTrue(res.success)
        response = res.data["response"]
        self.assertEqual(response["status"], 201)
        self.assertEqual(json.loads(response["body"])["body"], payload)

    def test_timeout(self):
        res = self.kernel.dispatch("network", "request", {
            "request": {
                "method": "GET",
                "url": "http://127.0.0.1:9999/timeout",
                "headers": {},
                "body": None,
                "timeout": 1 # Server sleeps for 2 seconds
            }
        })
        self.assertTrue(res.success)
        response = res.data["response"]
        self.assertIsNotNone(response["error"])
        self.assertIn("timeout", response["error"].lower())

    def test_invalid_url(self):
        res = self.kernel.dispatch("network", "request", {
            "request": {
                "method": "GET",
                "url": "http://invalid.local.domain",
                "timeout": 2
            }
        })
        self.assertTrue(res.success)
        response = res.data["response"]
        self.assertIsNotNone(response["error"])
        
    def test_concurrent_requests(self):
        results = []
        lock = threading.Lock()
        
        def worker():
            res = self.kernel.dispatch("network", "request", {
                "request": {
                    "method": "GET",
                    "url": "http://127.0.0.1:9999/api",
                    "timeout": 5
                }
            })
            with lock:
                results.append(res.success)
                
        threads = [threading.Thread(target=worker) for _ in range(50)]
        for t in threads: t.start()
        for t in threads: t.join()
        
        self.assertEqual(len(results), 50)
        self.assertTrue(all(results))

if __name__ == '__main__':
    unittest.main()
