import requests
import sqlite3
import json
import os
from aayu.runtime.stdlib.modules.auth_lib import mint_jwt

BASE_URL = "http://localhost:8000"

def setup_users():
    # Insert some dummy users with specific roles into aayu_auth_user table directly
    db_path = "db.sqlite3"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if not exists (in case it wasn't triggered by a registration call)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aayu_auth_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            roles TEXT DEFAULT '[]',
            permissions TEXT DEFAULT '[]'
        )
    """)
    
    # We will clear the users first just to be safe
    cursor.execute("DELETE FROM aayu_auth_user")
    
    # 1. Admin user
    cursor.execute(
        "INSERT INTO aayu_auth_user (email, password_hash, roles, permissions) VALUES (?, ?, ?, ?)",
        ("admin@aayu.dev", "hash", json.dumps(["admin"]), json.dumps([]))
    )
    admin_id = cursor.lastrowid
    
    # 2. Teacher user
    cursor.execute(
        "INSERT INTO aayu_auth_user (email, password_hash, roles, permissions) VALUES (?, ?, ?, ?)",
        ("teacher@aayu.dev", "hash", json.dumps(["teacher"]), json.dumps([]))
    )
    teacher_id = cursor.lastrowid
    
    # 3. Student user
    cursor.execute(
        "INSERT INTO aayu_auth_user (email, password_hash, roles, permissions) VALUES (?, ?, ?, ?)",
        ("student@aayu.dev", "hash", json.dumps(["student"]), json.dumps([]))
    )
    student_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return admin_id, teacher_id, student_id

def run_tests():
    admin_id, teacher_id, student_id = setup_users()
    
    admin_token = mint_jwt({"id": admin_id, "email": "admin@aayu.dev", "roles": ["admin"], "permissions": []})
    teacher_token = mint_jwt({"id": teacher_id, "email": "teacher@aayu.dev", "roles": ["teacher"], "permissions": []})
    student_token = mint_jwt({"id": student_id, "email": "student@aayu.dev", "roles": ["student"], "permissions": []})
    
    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    headers_teacher = {"Authorization": f"Bearer {teacher_token}"}
    headers_student = {"Authorization": f"Bearer {student_token}"}
    headers_none = {}
    
    print("Testing Security Enforcement...")
    
    # Test 1: No auth to Private resource
    # 'Document' has @role("teacher") and @auth (implicit)
    r = requests.get(f"{BASE_URL}/api/documents", headers=headers_none)
    assert r.status_code == 401, f"Expected 401, got {r.status_code}"
    print("Unauthenticated user blocked (401)")
    
    # Test 2: Student trying to access Teacher resource
    r = requests.get(f"{BASE_URL}/api/documents", headers=headers_student)
    assert r.status_code == 403, f"Expected 403, got {r.status_code}"
    print("Student blocked from Document (403 Forbidden)")
    
    # Test 3: Teacher accessing Teacher resource
    r = requests.get(f"{BASE_URL}/api/documents", headers=headers_teacher)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    print("Teacher allowed to access Document (200 OK)")
    
    # Test 4: Admin accessing Teacher resource
    r = requests.get(f"{BASE_URL}/api/documents", headers=headers_admin)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    print("Admin inherently allowed to access Document (200 OK)")

if __name__ == "__main__":
    run_tests()
