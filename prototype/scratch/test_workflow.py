import os
import sys
import subprocess
import sqlite3

def run_test():
    print(f"\n--- Running Test: workflow_engine ---")
    
    aayu_code = '''
workflow AppointmentWorkflow for Appointment.

step BookAppointment.
step DoctorReview.
step Prescription.
step Billing.
step Payment.

end.
'''
    
    # Write AAYU code
    test_file = "test_workflow.aayu"
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
        
        # Verify Workflow Table
        cursor.execute("SELECT id, name, entity_name FROM Workflow WHERE name = 'AppointmentWorkflow'")
        row = cursor.fetchone()
        if not row:
            print("[FAIL] Missing Workflow 'AppointmentWorkflow'")
            return False
            
        if row['entity_name'] != 'Appointment':
            print(f"[FAIL] Expected entity_name Appointment, got {row['entity_name']}")
            return False
            
        workflow_id = row['id']
                
        # Verify WorkflowStep Table
        cursor.execute("SELECT name, order_index FROM WorkflowStep WHERE workflow_id = ? ORDER BY order_index ASC", (workflow_id,))
        steps = cursor.fetchall()
        
        expected_steps = [
            "BookAppointment",
            "DoctorReview",
            "Prescription",
            "Billing",
            "Payment"
        ]
        
        found_steps = [s['name'] for s in steps]
        
        if found_steps != expected_steps:
            print(f"[FAIL] Expected steps {expected_steps}, got {found_steps}")
            return False
            
        # Verify WorkflowState table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='WorkflowState'")
        if not cursor.fetchone():
            print("[FAIL] Missing WorkflowState table")
            return False
            
        print("[OK] workflow_engine passed.")
        return True
            
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] workflow_engine raised CalledProcessError: {e}")
        if e.stderr:
            print(e.stderr.decode('utf-8'))
        return False
    except Exception as e:
        print(f"[FAIL] workflow_engine raised Exception: {e}")
        return False
    finally:
        if os.path.exists(test_file): os.remove(test_file)
        if os.path.exists(test_file.replace(".aayu", ".ayc")): os.remove(test_file.replace(".aayu", ".ayc"))


if __name__ == "__main__":
    # Clean DB
    if os.path.exists("aayu_db.sqlite"):
        os.remove("aayu_db.sqlite")
        
    run_test()
