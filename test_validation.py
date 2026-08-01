import urllib.request
import urllib.error
import json
import os
import time

def main():
    # Wait a bit for the server to spin up if called in script
    time.sleep(2)
    
    BASE_URL = "http://localhost:8000/api"
    headers = {"Content-Type": "application/json"}
    
    def request(method, path, data=None):
        req = urllib.request.Request(f"{BASE_URL}{path}", method=method, headers=headers)
        if data:
            req.data = json.dumps(data).encode('utf-8')
        try:
            with urllib.request.urlopen(req) as response:
                return response.getcode(), json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode())
        except Exception as e:
            return 500, str(e)
            
    print("Testing Validations...")
    
    # 1. Missing Required
    print("\n[Test 1] Missing Required Fields (POST)")
    code, res = request("POST", "/users", {"age": 20})
    print(f"Status: {code} | Response: {res}")
    assert code == 400
    assert "name" in res.get("errors", {})
    assert "email" in res.get("errors", {})
    
    # 2. Too small (min length)
    print("\n[Test 2] String too small (POST)")
    code, res = request("POST", "/users", {"name": "Ay", "email": "test@test.com"})
    print(f"Status: {code} | Response: {res}")
    assert code == 400
    assert "name" in res.get("errors", {})
    
    # 3. Invalid Type and Regex Mismatch
    print("\n[Test 3] Invalid Type & Regex Mismatch (POST)")
    code, res = request("POST", "/users", {"name": "Ayush", "email": "not-an-email", "age": "Twenty"})
    print(f"Status: {code} | Response: {res}")
    assert code == 400
    assert "email" in res.get("errors", {}) # regex
    assert "age" in res.get("errors", {}) # int
    
    # 4. Valid Creation
    print("\n[Test 4] Valid POST Creation")
    code, res = request("POST", "/users", {"name": "Ayush", "email": "ayush@test.com", "age": 25, "status": "Active"})
    print(f"Status: {code} | Response: {res}")
    assert code == 201
    user_id = res["data"]["id"]
    
    # 5. Invalid PATCH (Enum mismatch)
    print("\n[Test 5] Enum mismatch (PATCH)")
    code, res = request("PATCH", f"/users/{user_id}", {"status": "Pending"})
    print(f"Status: {code} | Response: {res}")
    assert code == 400
    assert "status" in res.get("errors", {})
    
    # 6. Valid PATCH (Partial update, omitting required fields)
    print("\n[Test 6] Valid PATCH (Partial Update)")
    code, res = request("PATCH", f"/users/{user_id}", {"age": 26})
    print(f"Status: {code} | Response: {res}")
    assert code == 200
    
    # 7. Invalid PUT (Missing required fields in full replacement)
    print("\n[Test 7] Invalid PUT (Missing Required)")
    code, res = request("PUT", f"/users/{user_id}", {"age": 27})
    print(f"Status: {code} | Response: {res}")
    assert code == 400
    assert "name" in res.get("errors", {})
    
    print("\nAll Validation Tests Passed! ✅")

if __name__ == "__main__":
    main()
