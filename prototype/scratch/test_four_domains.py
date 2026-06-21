import os
import sys
import time
import subprocess
import urllib.request
import urllib.parse
import threading

DOMAINS = [
    {"name": "patient", "entity": "Patient", "fields": {"name": "Ayush", "phone": "1234567890"}},
    {"name": "doctor", "entity": "Doctor", "fields": {"name": "Dr. Smith", "specialization": "Cardiology", "availability": "Mon-Fri"}},
    {"name": "product", "entity": "Product", "fields": {"title": "Laptop", "price": "999.99", "inventory": "50"}},
    {"name": "student", "entity": "Student", "fields": {"name": "Alice", "email": "alice@school.com", "course": "Computer Science"}}
]

def run_server(ayc_file):
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(".")
    process = subprocess.Popen([sys.executable, "-u", "cli.py", "vm", ayc_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, text=True)
    return process

for domain in DOMAINS:
    print(f"\n--- Testing Domain: {domain['entity']} ---")
    
    aayu_file = f"examples/crud_{domain['name']}.aayu"
    ayc_file = f"examples/crud_{domain['name']}.ayc"
    
    # 1. Compile
    res = subprocess.run([sys.executable, "cli.py", "compile", aayu_file], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[FAIL] Failed to compile {aayu_file}")
        print(res.stderr)
        continue
    print(f"[OK] Compiled {aayu_file}")
    
    # 2. Run Server
    proc = run_server(ayc_file)
    time.sleep(2) # wait for server to start
    
    try:
        # 3. GET request to verify UI generated
        get_url = f"http://localhost:8080/{domain['name']}s"
        req = urllib.request.Request(get_url)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            if f"{domain['entity']} Management" in html:
                print(f"[OK] GET {get_url} succeeded.")
            else:
                print(f"[FAIL] GET {get_url} failed to render correct HTML.")
                
        # 4. POST request to create record
        post_url = f"http://localhost:8080/{domain['name']}s/create"
        data = urllib.parse.urlencode(domain['fields']).encode('utf-8')
        req = urllib.request.Request(post_url, data=data, method="POST")
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Verify the newly created data is in the HTML table
            if list(domain['fields'].values())[0] in html:
                print(f"[OK] POST {post_url} succeeded and data persisted to DB -> UI.")
            else:
                print(f"[FAIL] POST {post_url} succeeded but data not found in UI.")
                
        # 5. PUT request to update record
        put_url = f"http://localhost:8080/{domain['name']}s/update"
        updated_fields = dict(domain['fields'])
        updated_fields[list(updated_fields.keys())[0]] = "UPDATED_VALUE"
        updated_fields['id'] = '1' # assuming it's the first record
        data = urllib.parse.urlencode(updated_fields).encode('utf-8')
        req = urllib.request.Request(put_url, data=data, method="PUT")
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            if "UPDATED_VALUE" in html:
                print(f"[OK] PUT {put_url} succeeded and data updated.")
            else:
                print(f"[FAIL] PUT {put_url} failed to reflect update in UI.")
                
        # 6. DELETE request to delete record
        delete_url = f"http://localhost:8080/{domain['name']}s/delete"
        data = urllib.parse.urlencode({'id': '1'}).encode('utf-8')
        req = urllib.request.Request(delete_url, data=data, method="DELETE")
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            if "UPDATED_VALUE" not in html:
                print(f"[OK] DELETE {delete_url} succeeded and data removed from UI.")
            else:
                print(f"[FAIL] DELETE {delete_url} failed to remove data.")

    except urllib.error.HTTPError as e:
        print(f"[FAIL] HTTP Error: {e.code} on {e.url}")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"[FAIL] Exception: {e}")
    finally:
        proc.terminate()
        try:
            outs, errs = proc.communicate(timeout=2)
            print(f"--- Server Logs for {domain['entity']} ---")
            print(outs)
        except Exception:
            pass
        proc.wait()
