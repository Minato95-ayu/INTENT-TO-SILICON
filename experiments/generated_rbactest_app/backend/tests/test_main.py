"""
=============================================================================
FILE: test_main.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from fastapi.testclient import TestClient

def test_health_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
