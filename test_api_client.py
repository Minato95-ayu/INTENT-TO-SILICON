import requests
import json
import time
import random

def test_api():
    print("Testing REST API generation...")
    email = f"test_{random.randint(1000, 9999)}@aayu.dev"
    password = "password123"
    
    # 1. Register a user
    print("\n--- POST /api/register ---")
    res = requests.post("http://localhost:8000/api/register", json={
        "e": email,
        "p": password
    })
    print("Status:", res.status_code)
    print("Response:", res.json())
    
    # 2. Login
    print("\n--- POST /api/login ---")
    res = requests.post("http://localhost:8000/api/login", json={
        "e": email,
        "p": password
    })
    print("Status:", res.status_code)
    print("Response:", res.json())
    
    token = res.json().get("data")
    if not token:
        print("Login failed, skipping authenticated endpoints.")
        return
        
    print(f"Token received: {token[:20]}...")
    
    # 3. Create Secret (Requires Auth)
    print("\n--- POST /api/createSecret ---")
    res = requests.post("http://localhost:8000/api/createSecret", json={
        "title": "My hidden treasure"
    }, headers={
        "Authorization": f"Bearer {token}"
    })
    print("Status:", res.status_code)
    print("Response:", res.json())
    
    # 4. View Secret (Requires Auth)
    print("\n--- POST /api/loadSecrets ---")
    res = requests.post("http://localhost:8000/api/loadSecrets", json={}, headers={
        "Authorization": f"Bearer {token}"
    })
    print("Status:", res.status_code)
    print("Response:", res.json())
    
    # 5. Bad payload test
    print("\n--- POST /api/register (Missing parameter) ---")
    res = requests.post("http://localhost:8000/api/register", json={
        "p": "pass"
    })
    print("Status:", res.status_code)
    print("Response:", res.json())
    
if __name__ == "__main__":
    test_api()
