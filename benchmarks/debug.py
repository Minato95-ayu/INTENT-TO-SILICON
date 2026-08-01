import subprocess
import time
import urllib.request
import json

p = subprocess.Popen(['python', '-u', '../../aayu/cli.py', 'run'], cwd='aayu_app', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2)
try:
    req = urllib.request.Request('http://127.0.0.1:8000/api/login', data=json.dumps({"email":"test","password":"test"}).encode(), headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)
except Exception as e:
    print('Error:', e)

p.kill()
out, err = p.communicate()
print('STDOUT:')
print(out.decode())
print('STDERR:')
print(err.decode())
