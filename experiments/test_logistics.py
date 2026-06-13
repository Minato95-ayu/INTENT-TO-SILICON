import sqlite3
import requests
import time
import sys

BASE_URL = "http://localhost:8000/api"

def test_logistics():
    print("Testing Vehicle Creation...")
    vehicle_data = {
        "license_plate": "XYZ-1234",
        "capacity": "10 Tons"
    }
    r = requests.post(f"{BASE_URL}/vehicle", json=vehicle_data)
    if r.status_code != 200:
        print(f"Failed: {r.text}")
        sys.exit(1)
    vehicle = r.json()
    print("POST /api/vehicle -> 200")

    print("Testing Driver Creation...")
    driver_data = {
        "name": "Alex Mercer",
        "license_number": "DL-98765"
    }
    r = requests.post(f"{BASE_URL}/driver", json=driver_data)
    if r.status_code != 200:
        print(f"Failed: {r.text}")
        sys.exit(1)
    driver = r.json()
    print("POST /api/driver -> 200")

    print("Testing Shipment Creation...")
    shipment_data = {
        "tracking_number": "TRK-999",
        "carrier": "FastCourier",
        "status": "In Transit",
        "vehicle_id": vehicle["id"],
        "driver_id": driver["id"]
    }
    r = requests.post(f"{BASE_URL}/shipment", json=shipment_data)
    if r.status_code != 200:
        print(f"Failed: {r.text}")
        sys.exit(1)
    shipment = r.json()
    print("POST /api/shipment -> 200")

    print("Testing Warehouse Creation...")
    warehouse_data = {
        "name": "Central Hub",
        "location": "Downtown",
        "capacity": 50000
    }
    r = requests.post(f"{BASE_URL}/warehouse", json=warehouse_data)
    if r.status_code != 200:
        print(f"Failed: {r.text}")
        sys.exit(1)
    warehouse = r.json()
    print("POST /api/warehouse -> 200")

    print("Testing Delivery Creation...")
    delivery_data = {
        "delivery_date": "2026-06-15T10:00:00",
        "recipient_signature": "John Smith",
        "shipment_id": shipment["id"],
        "warehouse_id": warehouse["id"]
    }
    r = requests.post(f"{BASE_URL}/delivery", json=delivery_data)
    if r.status_code != 200:
        print(f"Failed: {r.text}")
        sys.exit(1)
    delivery = r.json()
    print("POST /api/delivery -> 200")

    print("\nVerifying directly in SQLite Database...")
    conn = sqlite3.connect("generated_project/backend/aayu_generated.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM vehicle WHERE id = ?", (vehicle["id"],))
    assert cursor.fetchone() is not None
    
    cursor.execute("SELECT * FROM driver WHERE id = ?", (driver["id"],))
    assert cursor.fetchone() is not None
    
    cursor.execute("SELECT * FROM shipment WHERE id = ?", (shipment["id"],))
    assert cursor.fetchone() is not None

    cursor.execute("SELECT * FROM warehouse WHERE id = ?", (warehouse["id"],))
    assert cursor.fetchone() is not None

    cursor.execute("SELECT * FROM delivery WHERE id = ?", (delivery["id"],))
    assert cursor.fetchone() is not None
    
    conn.close()
    print("\nAll Tests Passed Successfully! Logistics CRUD Reality Check Verified.")

if __name__ == "__main__":
    time.sleep(1)
    try:
        test_logistics()
    except requests.exceptions.ConnectionError:
        print("Error: FastAPI server is not running. Please start it on port 8000.")
        sys.exit(1)
