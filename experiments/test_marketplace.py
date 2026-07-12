"""
=============================================================================
FILE: test_marketplace.py
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

def test_marketplace():
    if not wait_for_server():
        print("Server did not start")
        sys.exit(1)
        
    print("Testing Seller Creation...")
    resp = requests.post(f"{BASE_URL}/api/seller", json={
        "name": "Super Electronics",
        "gst_number": "GST12345",
        "rating": 4.8
    })
    print(f"POST /api/seller -> {resp.status_code}")
    assert resp.status_code == 200
    seller = resp.json()
    
    print("Testing Product Creation...")
    resp = requests.post(f"{BASE_URL}/api/product", json={
        "name": "Laptop Pro",
        "price": 1200.0,
        "stock_quantity": 50,
        "seller_id": seller["id"]
    })
    print(f"POST /api/product -> {resp.status_code}")
    assert resp.status_code == 200
    product = resp.json()
    
    print("Testing Buyer Creation...")
    resp = requests.post(f"{BASE_URL}/api/buyer", json={
        "name": "Alice Corp",
        "company_name": "Alice Corp Inc"
    })
    print(f"POST /api/buyer -> {resp.status_code}")
    assert resp.status_code == 200
    buyer = resp.json()
    
    print("Testing Order Creation...")
    resp = requests.post(f"{BASE_URL}/api/order", json={
        "total_amount": 1200.0,
        "status": "Pending",
        "buyer_id": buyer["id"],
        "product_id": product["id"]
    })
    print(f"POST /api/order -> {resp.status_code}")
    assert resp.status_code == 200
    order = resp.json()
    
    # Verify in DB
    print("\nVerifying directly in SQLite Database...")
    
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'generated_project', 'backend', 'aayu_generated.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM seller WHERE id = ?", (seller["id"],))
    assert cursor.fetchone() is not None
    
    cursor.execute('SELECT * FROM "order" WHERE id = ?', (order["id"],))
    assert cursor.fetchone() is not None
    
    conn.close()
    print("\nAll Tests Passed Successfully! Marketplace CRUD Reality Check Verified.")

if __name__ == "__main__":
    test_marketplace()
