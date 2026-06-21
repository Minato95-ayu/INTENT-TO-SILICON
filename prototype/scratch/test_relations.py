import os
import sys
import subprocess
import sqlite3
import time

def run_test(name, aayu_code, verify_fn):
    print(f"\n--- Running Test: {name} ---")
    
    # Write AAYU code
    test_file = f"test_{name}.aayu"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(aayu_code)
        
    # Run compiler and VM
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.abspath(".")
        
        # Compile
        subprocess.run([sys.executable, "cli.py", "compile", test_file], env=env, check=True, capture_output=True)
        
        # Run VM (it will generate the DB schema and exit because there is no 'serve' command)
        ayc_file = test_file.replace(".aayu", ".ayc")
        subprocess.run([sys.executable, "cli.py", "vm", ayc_file], env=env, check=True, capture_output=True)
        
        # Verify schema
        conn = sqlite3.connect("aayu_db.sqlite")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if verify_fn(cursor):
            print(f"[OK] {name} passed.")
        else:
            print(f"[FAIL] {name} failed schema verification.")
            
        conn.close()
        
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] {name} raised CalledProcessError: {e}")
        if e.stderr:
            print(e.stderr.decode('utf-8'))
    except Exception as e:
        print(f"[FAIL] {name} raised Exception: {e}")
    finally:
        if os.path.exists(test_file): os.remove(test_file)
        if os.path.exists(test_file.replace(".aayu", ".ayc")): os.remove(test_file.replace(".aayu", ".ayc"))


def verify_many_to_many(cursor):
    # Should have Student_Course table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Student_Course'")
    if not cursor.fetchone():
        print("Missing table Student_Course")
        return False
    
    # Check columns
    cursor.execute("PRAGMA table_info(Student_Course)")
    cols = [r['name'] for r in cursor.fetchall()]
    expected = ['id', 'student_id', 'course_id', 'created_at', 'updated_at']
    for e in expected:
        if e not in cols:
            print(f"Missing column {e} in Student_Course")
            return False
            
    return True

def verify_one_to_many(cursor):
    # Doctor one_to_many Appointment -> Appointment should have doctor_id
    cursor.execute("PRAGMA table_info(Appointment)")
    cols = [r['name'] for r in cursor.fetchall()]
    if 'doctor_id' not in cols:
        print("Missing doctor_id in Appointment")
        return False
    return True

def verify_one_to_one(cursor):
    # User one_to_one Profile -> Profile should have user_id
    cursor.execute("PRAGMA table_info(Profile)")
    cols = [r['name'] for r in cursor.fetchall()]
    if 'user_id' not in cols:
        print("Missing user_id in Profile")
        return False
    return True

if __name__ == "__main__":
    # Clean DB
    if os.path.exists("aayu_db.sqlite"):
        os.remove("aayu_db.sqlite")
        
    # Test 1: Many to Many
    code1 = '''
entity Student.
    text name.
end.

entity Course.
    text title.
end.

relation Student many_to_many Course.
'''
    run_test("many_to_many", code1, verify_many_to_many)
    
    # Test 2: One to Many
    code2 = '''
entity Doctor.
    text name.
end.

entity Appointment.
    text date.
end.

relation Doctor one_to_many Appointment.
'''
    run_test("one_to_many", code2, verify_one_to_many)
    
    # Test 3: One to One
    code3 = '''
entity User.
    text email.
end.

entity Profile.
    text bio.
end.

relation User one_to_one Profile.
'''
    run_test("one_to_one", code3, verify_one_to_one)
