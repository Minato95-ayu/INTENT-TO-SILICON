"""
=============================================================================
FILE: test_agriculture.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import sqlite3
import requests
import time
import sys

BASE_URL = "http://localhost:8000/api"

def test_agriculture():
    print("Testing Farmer Creation...")
    farmer_data = {
        "name": "John Doe",
        "phone": "555-0199",
        "location": "Springfield"
    }
    r = requests.post(f"{BASE_URL}/farmer", json=farmer_data)
    if r.status_code != 200:
        print(f"Failed: {r.text}")
        sys.exit(1)
    farmer = r.json()
    print("POST /api/farmer -> 200")

    print("Testing Farm Plot Creation...")
    farm_plot_data = {
        "size_acres": 50.5,
        "soil_type": "Loam",
        "farmer_id": farmer["id"]
    }
    r = requests.post(f"{BASE_URL}/farm_plot", json=farm_plot_data)
    if r.status_code != 200:
        print(f"Failed: {r.text}")
        sys.exit(1)
    farm_plot = r.json()
    print("POST /api/farm_plot -> 200")

    print("Testing Crop Log Creation...")
    crop_log_data = {
        "crop_name": "Wheat",
        "plant_date": "2026-06-01T00:00:00",
        "expected_yield": 200.5,
        "farm_plot_id": farm_plot["id"]
    }
    r = requests.post(f"{BASE_URL}/crop_log", json=crop_log_data)
    if r.status_code != 200:
        print(f"Failed: {r.text}")
        sys.exit(1)
    crop_log = r.json()
    print("POST /api/crop_log -> 200")

    print("\nVerifying directly in SQLite Database...")
    conn = sqlite3.connect("generated_project/backend/aayu_generated.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM farmer WHERE id = ?", (farmer["id"],))
    assert cursor.fetchone() is not None
    
    cursor.execute("SELECT * FROM farm_plot WHERE id = ?", (farm_plot["id"],))
    assert cursor.fetchone() is not None
    
    cursor.execute("SELECT * FROM crop_log WHERE id = ?", (crop_log["id"],))
    assert cursor.fetchone() is not None
    
    conn.close()
    print("\nAll Tests Passed Successfully! Agriculture CRUD Reality Check Verified.")

if __name__ == "__main__":
    # Give the server a second to start
    time.sleep(1)
    try:
        test_agriculture()
    except requests.exceptions.ConnectionError:
        print("Error: FastAPI server is not running. Please start it on port 8000.")
        sys.exit(1)
