import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing Auto CRUD APIs...")

    # 1. Create a User
    print("\n--- POST /api/users ---")
    payload = {
        "name": "Ayush",
        "email": "ayush@aayu.dev",
        "age": 25
    }
    r = requests.post(f"{BASE_URL}/api/users", json=payload)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    user_id = r.json().get("data", {}).get("id")

    # 2. Read the User
    if user_id:
        print(f"\n--- GET /api/users/{user_id} ---")
        r = requests.get(f"{BASE_URL}/api/users/{user_id}")
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")

    # 3. List Users
    print("\n--- GET /api/users ---")
    r = requests.get(f"{BASE_URL}/api/users")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")

    # 4. Search Users
    print("\n--- GET /api/users?q=Ayush ---")
    r = requests.get(f"{BASE_URL}/api/users?q=Ayush")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    
    print("\n--- GET /api/users?age>18 ---")
    r = requests.get(f"{BASE_URL}/api/users?age>18")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")

    # 5. Update User
    if user_id:
        print(f"\n--- PUT /api/users/{user_id} ---")
        payload = {"name": "Ayush (Updated)", "email": "ayush@aayu.dev", "age": 26}
        r = requests.put(f"{BASE_URL}/api/users/{user_id}", json=payload)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")

    # 6. Delete User
    if user_id:
        print(f"\n--- DELETE /api/users/{user_id} ---")
        r = requests.delete(f"{BASE_URL}/api/users/{user_id}")
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")

    # 7. Check Exists
    if user_id:
        print(f"\n--- GET /api/users/exists?id={user_id} ---")
        r = requests.get(f"{BASE_URL}/api/users/exists?id={user_id}")
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")

if __name__ == '__main__':
    test_api()
