import os
import sys
import subprocess
import sqlite3

def run_test():
    print(f"\n--- Running Test: rbac_engine ---")
    
    aayu_code = '''
role Admin.
role Doctor.
role Patient.

allow Doctor create Prescription.
allow Doctor view Patient.
allow Patient view Prescription.
'''
    
    # Write AAYU code
    test_file = "test_rbac.aayu"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(aayu_code)
        
    # Run compiler and VM
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.abspath(".")
        
        # Compile
        subprocess.run([sys.executable, "cli.py", "compile", test_file], env=env, check=True, capture_output=True)
        
        # Run VM
        ayc_file = test_file.replace(".aayu", ".ayc")
        subprocess.run([sys.executable, "cli.py", "vm", ayc_file], env=env, check=True, capture_output=True)
        
        # Verify schema
        conn = sqlite3.connect("aayu_db.sqlite")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Verify Role Table
        cursor.execute("SELECT name FROM Role")
        roles = [r['name'] for r in cursor.fetchall()]
        expected_roles = ["Admin", "Doctor", "Patient"]
        for r in expected_roles:
            if r not in roles:
                print(f"[FAIL] Missing role {r}")
                return False
                
        # Verify Permission Table
        cursor.execute("""
            SELECT Role.name as role_name, Permission.action, Permission.resource_name 
            FROM Permission 
            JOIN Role ON Permission.role_id = Role.id
        """)
        permissions = cursor.fetchall()
        
        expected_permissions = [
            ("Doctor", "create", "Prescription"),
            ("Doctor", "view", "Patient"),
            ("Patient", "view", "Prescription")
        ]
        
        found_perms = [(p['role_name'], p['action'], p['resource_name']) for p in permissions]
        
        for ep in expected_permissions:
            if ep not in found_perms:
                print(f"[FAIL] Missing permission {ep}")
                return False
                
        print("[OK] rbac_engine passed.")
        return True
            
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] rbac_engine raised CalledProcessError: {e}")
        if e.stderr:
            print(e.stderr.decode('utf-8'))
        return False
    except Exception as e:
        print(f"[FAIL] rbac_engine raised Exception: {e}")
        return False
    finally:
        if os.path.exists(test_file): os.remove(test_file)
        if os.path.exists(test_file.replace(".aayu", ".ayc")): os.remove(test_file.replace(".aayu", ".ayc"))


if __name__ == "__main__":
    # Clean DB
    if os.path.exists("aayu_db.sqlite"):
        os.remove("aayu_db.sqlite")
        
    run_test()
