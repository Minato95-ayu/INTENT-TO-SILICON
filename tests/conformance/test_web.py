import unittest
import threading
import time
import json
import urllib.request
import urllib.error
from typing import Any, Dict
from aayu.runtime.kernel.interface import DispatchResult
from aayu.runtime.kernel.core import RuntimeKernel
from aayu.runtime.plugins.web.runtime import WebRuntime

class TestWebRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kernel = RuntimeKernel()
        cls.web = WebRuntime(port=8888)
        cls.kernel.registry.register(cls.web)
        cls.kernel.boot()
        
        # Wait for server to boot
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.kernel.shutdown()

    def setUp(self):
        # Clear routes and middlewares for each test
        self.web.routes = {
            "GET": {}, "POST": {}, "PUT": {}, "DELETE": {}, "PATCH": {}
        }
        self.web.middlewares = []

    def request(self, method, path):
        req = urllib.request.Request(f"http://127.0.0.1:8888{path}", method=method)
        try:
            with urllib.request.urlopen(req, timeout=2) as res:
                return res.status, res.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode('utf-8')

    def test_route_registration_and_200(self):
        def handler(req, res):
            res["status"] = 200
            res["body"] = "Hello AAYU"
            
        self.kernel.dispatch("web", "route", {
            "method": "GET",
            "path": "/hello",
            "handler": handler
        })
        
        status, body = self.request("GET", "/hello")
        self.assertEqual(status, 200)
        self.assertEqual(body, "Hello AAYU")

    def test_404_not_found(self):
        status, _ = self.request("GET", "/does-not-exist")
        self.assertEqual(status, 404)

    def test_500_internal_error(self):
        def crashy_handler(req, res):
            raise ValueError("Intentional crash")
            
        self.kernel.dispatch("web", "route", {
            "method": "GET",
            "path": "/crash",
            "handler": crashy_handler
        })
        
        status, _ = self.request("GET", "/crash")
        self.assertEqual(status, 500)

    def test_middleware_chain(self):
        # Middleware 1: adds a header
        def mid1(req, res, next_func):
            res["headers"]["X-Mid-1"] = "true"
            next_func()
            
        # Middleware 2: aborts if auth missing
        def mid2(req, res, next_func):
            if req["headers"].get("Authorization") != "secret":
                res["status"] = 401
                res["body"] = "Unauthorized"
                return
            next_func()
            
        self.kernel.dispatch("web", "middleware", {"handler": mid1})
        self.kernel.dispatch("web", "middleware", {"handler": mid2})
        
        def handler(req, res):
            res["status"] = 200
            res["body"] = "Secret Area"
            
        self.kernel.dispatch("web", "route", {
            "method": "GET",
            "path": "/secret",
            "handler": handler
        })
        
        # Test without auth (should be blocked by mid2)
        status, body = self.request("GET", "/secret")
        self.assertEqual(status, 401)
        self.assertEqual(body, "Unauthorized")
        
        # Test with auth
        req = urllib.request.Request("http://127.0.0.1:8888/secret", headers={"Authorization": "secret"})
        with urllib.request.urlopen(req) as r:
            self.assertEqual(r.status, 200)
            self.assertEqual(r.headers["X-Mid-1"], "true")
            self.assertEqual(r.read().decode('utf-8'), "Secret Area")

    def test_concurrent_clients(self):
        def slow_handler(req, res):
            time.sleep(0.1)
            res["status"] = 200
            res["body"] = "done"
            
        self.kernel.dispatch("web", "route", {
            "method": "GET",
            "path": "/slow",
            "handler": slow_handler
        })
        
        results = []
        lock = threading.Lock()
        
        def worker():
            status, body = self.request("GET", "/slow")
            with lock:
                results.append((status, body))
                
        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads: t.start()
        for t in threads: t.join()
        
        self.assertEqual(len(results), 20)
        self.assertTrue(all(r[0] == 200 for r in results))

if __name__ == '__main__':
    unittest.main()
