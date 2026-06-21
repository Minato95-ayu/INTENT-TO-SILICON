import os
import sys
import subprocess
import sqlite3
import time
import urllib.request
import threading

def run_test():
    print(f"\n--- Running Test: Hospital Demo ---")
    
    demo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hospital_demo"))
    main_file = os.path.join(demo_dir, "main.aayu")
    db_file = os.path.join(demo_dir, "aayu_db.sqlite")
    
    # Clean DB
    if os.path.exists(db_file):
        os.remove(db_file)
        
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        # 1. Compile
        print("Compiling main.aayu...")
        subprocess.run([sys.executable, "../cli.py", "compile", "main.aayu"], cwd=demo_dir, env=env, check=True, capture_output=True)
        
        # 2. Run VM in background
        print("Starting VM...")
        ayc_file = "main.ayc"
        vm_process = subprocess.Popen([sys.executable, "../cli.py", "vm", ayc_file], cwd=demo_dir, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it a second to start the server
        time.sleep(2)
        
        # 3. Verify SQLite Tables
        print("Verifying SQLite Tables...")
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Verify Entities (check if tables exist)
        tables_to_check = ['Patient', 'Doctor', 'Appointment', 'Prescription', 'Invoice', 'Payment']
        for t in tables_to_check:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (t,))
            if not cursor.fetchone():
                print(f"[FAIL] Missing Entity table: {t}")
                vm_process.kill()
                return False
                
        # Verify Relations (check columns)
        # Appointment should have patient_id and doctor_id
        cursor.execute("PRAGMA table_info(Appointment)")
        columns = [row['name'] for row in cursor.fetchall()]
        if 'patient_id' not in columns or 'doctor_id' not in columns:
            print(f"[FAIL] Missing relation columns in Appointment: {columns}")
            vm_process.kill()
            return False
            
        # Verify RBAC
        cursor.execute("SELECT name FROM Role")
        roles = [r['name'] for r in cursor.fetchall()]
        if 'Admin' not in roles or 'Doctor' not in roles:
            print(f"[FAIL] Missing roles: {roles}")
            vm_process.kill()
            return False
            
        cursor.execute("SELECT count(*) as c FROM Permission")
        if cursor.fetchone()['c'] < 5:
            print("[FAIL] Missing permissions")
            vm_process.kill()
            return False
            
        # Verify Workflows
        cursor.execute("SELECT count(*) as c FROM WorkflowStep")
        if cursor.fetchone()['c'] < 5:
            print("[FAIL] Missing workflow steps")
            vm_process.kill()
            return False
            
        # 4. Verify HTTP Server (CRUD & UI)
        print("Verifying HTTP Routes...")
        
        # Dashboard
        req = urllib.request.Request("http://localhost:8080/dashboard")
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            if "Hospital Management System" not in html or "Patients" not in html:
                print("[FAIL] Dashboard UI not rendered correctly")
                vm_process.kill()
                return False
                
        # CRUD Route
        req = urllib.request.Request("http://localhost:8080/patients")
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            if "Patient" not in html:
                print("[FAIL] Patient CRUD UI not rendered correctly")
                vm_process.kill()
                return False
                
        print("[OK] Hospital Demo Verification Passed! SUCCESS")
        
    except Exception as e:
        print(f"[FAIL] Exception: {e}")
        return False
    finally:
        if 'vm_process' in locals():
            vm_process.kill()

if __name__ == "__main__":
    run_test()
