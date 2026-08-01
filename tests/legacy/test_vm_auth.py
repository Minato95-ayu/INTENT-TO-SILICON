"""
=============================================================================
FILE: test_vm_auth.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import sys
import unittest
import urllib.request
import urllib.parse
import http.cookiejar
import threading
import time
import sqlite3
import datetime
from urllib.error import HTTPError

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "aayu_language"))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from vm import VirtualMachine

class TestVMAuthentication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tests_dir = os.path.dirname(__file__)
        cls.db_path = os.path.join(cls.tests_dir, "..", "aayu_db.sqlite")
        cls.filepath = os.path.join(cls.tests_dir, "test_auth.aayu")
        
        # Compile test_auth.aayu
        with open(cls.filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=cls.filepath)
        ast = parser.parse()
        compiler = BytecodeEncoder()
        cls.bytecode = compiler.compile(ast)

    def setUp(self):
        # Ensure clean DB for each test
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except Exception:
                pass
        self.vm = None
        self.port = 8081

    def tearDown(self):
        self.stop_server()
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except Exception:
                pass

    def start_server(self):
        self.vm = VirtualMachine(db_path=self.db_path)
        # Since test_auth.aayu runs a blocking HTTP server via 'serve on 8081',
        # we start the virtual machine execution in a background thread.
        self.server_thread = threading.Thread(
            target=self.vm.run,
            args=(self.bytecode,)
        )
        self.server_thread.daemon = True
        self.server_thread.start()
        # Allow server to boot
        time.sleep(0.5)

    def stop_server(self):
        if self.vm:
            if hasattr(self.vm, "http_server") and self.vm.http_server:
                try:
                    self.vm.http_server.shutdown()
                    self.vm.http_server.server_close()
                except Exception:
                    pass
            try:
                self.vm.close()
            except Exception:
                pass
        self.vm = None

    def test_01_dashboard_unauthorized(self):
        """Accessing dashboard without session must fail with 401."""
        self.start_server()
        req = urllib.request.Request(f"http://localhost:{self.port}/dashboard")
        try:
            urllib.request.urlopen(req)
            self.fail("Expected 401 Unauthorized")
        except HTTPError as e:
            self.assertEqual(e.code, 401)

    def test_02_registration_success(self):
        """User registration should return 200 OK and persist the user in DB."""
        self.start_server()
        reg_data = urllib.parse.urlencode({"email": "reg@test.com", "password": "pw"}).encode()
        req = urllib.request.Request(f"http://localhost:{self.port}/register", data=reg_data, method="POST")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("Registered", resp.read().decode())

    def test_03_registration_duplicate(self):
        """Registering duplicate email should return 500 error."""
        self.start_server()
        reg_data = urllib.parse.urlencode({"email": "dup@test.com", "password": "pw"}).encode()
        req = urllib.request.Request(f"http://localhost:{self.port}/register", data=reg_data, method="POST")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
        try:
            urllib.request.urlopen(req)
            self.fail("Expected duplicate email to fail")
        except HTTPError as e:
            self.assertEqual(e.code, 500)

    def test_04_login_invalid_credentials(self):
        """Login with non-existent email or wrong password must return 401."""
        self.start_server()
        
        # 1. Non-existent email
        login_data = urllib.parse.urlencode({"email": "missing@test.com", "password": "pw"}).encode()
        req = urllib.request.Request(f"http://localhost:{self.port}/login", data=login_data, method="POST")
        try:
            urllib.request.urlopen(req)
            self.fail("Expected 401")
        except HTTPError as e:
            self.assertEqual(e.code, 401)

        # 2. Existing email, wrong password
        reg_data = urllib.parse.urlencode({"email": "wrongpw@test.com", "password": "correctpw"}).encode()
        urllib.request.urlopen(urllib.request.Request(f"http://localhost:{self.port}/register", data=reg_data, method="POST"))
        
        login_wrong = urllib.parse.urlencode({"email": "wrongpw@test.com", "password": "badpw"}).encode()
        req_wrong = urllib.request.Request(f"http://localhost:{self.port}/login", data=login_wrong, method="POST")
        try:
            urllib.request.urlopen(req_wrong)
            self.fail("Expected 401")
        except HTTPError as e:
            self.assertEqual(e.code, 401)

    def test_05_login_success(self):
        """Valid login should set a secure session cookie."""
        self.start_server()
        
        reg_data = urllib.parse.urlencode({"email": "login@test.com", "password": "pw"}).encode()
        urllib.request.urlopen(urllib.request.Request(f"http://localhost:{self.port}/register", data=reg_data, method="POST"))
        
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        login_data = urllib.parse.urlencode({"email": "login@test.com", "password": "pw"}).encode()
        req = urllib.request.Request(f"http://localhost:{self.port}/login", data=login_data, method="POST")
        with opener.open(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("Logged In", resp.read().decode())

        cookie_names = [c.name for c in cj]
        self.assertIn("AAYU_SESSION", cookie_names)

    def test_06_dashboard_authorized(self):
        """Accessing dashboard with a valid session cookie must succeed."""
        self.start_server()
        
        reg_data = urllib.parse.urlencode({"email": "dash@test.com", "password": "pw"}).encode()
        urllib.request.urlopen(urllib.request.Request(f"http://localhost:{self.port}/register", data=reg_data, method="POST"))
        
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        login_data = urllib.parse.urlencode({"email": "dash@test.com", "password": "pw"}).encode()
        opener.open(urllib.request.Request(f"http://localhost:{self.port}/login", data=login_data, method="POST"))

        req = urllib.request.Request(f"http://localhost:{self.port}/dashboard")
        with opener.open(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("Welcome to Dashboard", resp.read().decode())

    def test_07_logout_invalidates_session(self):
        """Logout must delete the session token from DB and clear cookie."""
        self.start_server()
        
        reg_data = urllib.parse.urlencode({"email": "logout@test.com", "password": "pw"}).encode()
        urllib.request.urlopen(urllib.request.Request(f"http://localhost:{self.port}/register", data=reg_data, method="POST"))
        
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        login_data = urllib.parse.urlencode({"email": "logout@test.com", "password": "pw"}).encode()
        opener.open(urllib.request.Request(f"http://localhost:{self.port}/login", data=login_data, method="POST"))

        # Verify active session
        with opener.open(urllib.request.Request(f"http://localhost:{self.port}/dashboard")) as resp:
            self.assertIn("Welcome to Dashboard", resp.read().decode())

        # Perform logout
        with opener.open(urllib.request.Request(f"http://localhost:{self.port}/logout", data=b"", method="POST")) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("Logged Out", resp.read().decode())

        # Dashboard access should now fail
        try:
            opener.open(urllib.request.Request(f"http://localhost:{self.port}/dashboard"))
            self.fail("Expected 401 Unauthorized after logout")
        except HTTPError as e:
            self.assertEqual(e.code, 401)

    def test_08_session_persistence_restart(self):
        """Sessions must survive VM restart (database backed)."""
        self.start_server()
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

        reg_data = urllib.parse.urlencode({"email": "persist@test.com", "password": "pw"}).encode()
        opener.open(urllib.request.Request(f"http://localhost:{self.port}/register", data=reg_data, method="POST"))

        login_data = urllib.parse.urlencode({"email": "persist@test.com", "password": "pw"}).encode()
        opener.open(urllib.request.Request(f"http://localhost:{self.port}/login", data=login_data, method="POST"))

        session_cookie = next(c for c in cj if c.name == "AAYU_SESSION")
        token_value = session_cookie.value

        # Stop VM
        self.stop_server()
        time.sleep(0.5)

        # Start VM again (preserving DB file)
        self.start_server()

        # Try to access protected route with the same cookie passed directly in the header
        req = urllib.request.Request(f"http://localhost:{self.port}/dashboard")
        req.add_header("Cookie", f"AAYU_SESSION={token_value}")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("Welcome to Dashboard", resp.read().decode())

if __name__ == "__main__":
    unittest.main()
