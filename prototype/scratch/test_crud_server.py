import urllib.request
import threading
import sys
import subprocess
import time

import os

def run_server():
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(".")
    process = subprocess.Popen([sys.executable, "-u", "cli.py", "vm", "test_crud.ayc"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, text=True)
    for line in iter(process.stdout.readline, ''):
        print("SERVER LOG:", line, end='')

t = threading.Thread(target=run_server, daemon=True)
t.start()

time.sleep(2)
try:
    req = urllib.request.Request('http://localhost:8080/patients')
    with urllib.request.urlopen(req) as response:
        print("SUCCESS:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print(e.read().decode('utf-8'))
except Exception as e:
    print("OTHER ERROR:", e)
