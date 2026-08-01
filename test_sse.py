import requests
import json
import time

try:
    print("Testing /api/event with ACTION add_camera")
    res = requests.post("http://localhost:3000/api/event", json={"type": "ACTION", "target": "add_camera"})
    print(res.status_code, res.text)
    
except Exception as e:
    print(e)
