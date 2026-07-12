"""
=============================================================================
FILE: test_auth.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import pytest
import uuid
from fastapi.testclient import TestClient

def test_register(client: TestClient):
    payload = {
        "email": f"test_{uuid.uuid4()}@example.com",
        "password": "strongpassword123"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    return payload

def test_duplicate_register(client: TestClient):
    payload = test_register(client)
    # Trying to register again with same email
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400

def test_login(client: TestClient):
    payload = test_register(client)
    # Login with correct credentials
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid(client: TestClient):
    payload = test_register(client)
    payload["password"] = "wrongpassword"
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
