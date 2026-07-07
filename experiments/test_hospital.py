"""
=============================================================================
FILE: test_hospital.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import requests
import sqlite3
import time
import sys
import os

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server():
    for _ in range(10):
        try:
            requests.get(f"{BASE_URL}/")
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    return False

def test_hospital():
    if not wait_for_server():
        print("Server did not start")
        sys.exit(1)
        
    print("Testing Patient Creation...")
    resp = requests.post(f"{BASE_URL}/api/patient", json={
        "name": "John Doe",
        "age": 45,
        "gender": "Male"
    })
    print(f"POST /api/patient -> {resp.status_code}")
    assert resp.status_code == 200
    patient = resp.json()
    print("Patient Response:", patient)
    
    print("Testing Doctor Creation...")
    resp = requests.post(f"{BASE_URL}/api/doctor", json={
        "name": "Dr. Smith",
        "specialization": "Cardiology",
        "phone": "555-0192"
    })
    print(f"POST /api/doctor -> {resp.status_code}")
    assert resp.status_code == 200
    doctor = resp.json()
    print("Doctor Response:", doctor)
    
    print("Testing Appointment Creation...")
    resp = requests.post(f"{BASE_URL}/api/appointment", json={
        "appointment_date": "2026-06-15T10:00:00",
        "status": "Scheduled",
        "patient_id": patient["id"],
        "doctor_id": doctor["id"]
    })
    print(f"POST /api/appointment -> {resp.status_code}")
    assert resp.status_code == 200
    appointment = resp.json()
    print("Appointment Response:", appointment)
    
    # Verify in DB
    print("\nVerifying directly in SQLite Database...")
    
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'generated_project', 'backend', 'aayu_generated.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM patient WHERE id = ?", (patient["id"],))
    db_patient = cursor.fetchone()
    print("DB Patient:", db_patient)
    assert db_patient is not None
    
    cursor.execute("SELECT * FROM doctor WHERE id = ?", (doctor["id"],))
    db_doctor = cursor.fetchone()
    print("DB Doctor:", db_doctor)
    assert db_doctor is not None
    
    cursor.execute("SELECT * FROM appointment WHERE id = ?", (appointment["id"],))
    db_appt = cursor.fetchone()
    print("DB Appointment:", db_appt)
    assert db_appt is not None
    
    conn.close()
    print("\nAll Tests Passed Successfully! CRUD Reality Check Verified.")

if __name__ == "__main__":
    test_hospital()
