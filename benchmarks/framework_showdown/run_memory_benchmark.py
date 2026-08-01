import subprocess
import time
import psutil
import requests
import os
import signal

def measure_app(command, port, name):
    print(f"\n--- Measuring {name} ---")
    
    start_time = time.time()
    process = subprocess.Popen(command, shell=True)
    
    # Wait for startup
    startup_time = 0
    while True:
        try:
            requests.options(f"http://127.0.0.1:{port}")
            startup_time = (time.time() - start_time) * 1000
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.01)
            if time.time() - start_time > 5:
                print("Failed to start")
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
                return
                
    # Measure Idle Memory
    p = psutil.Process(process.pid)
    memory_mb = p.memory_info().rss / (1024 * 1024)
    
    print(f"Startup Time: {startup_time:.2f} ms")
    print(f"Idle Memory: {memory_mb:.2f} MB")
    
    # Measure Latency
    latencies = []
    for _ in range(30):
        t0 = time.time()
        # Ensure the endpoint exists or catch 404, we just want network roundtrip latency
        try:
            requests.options(f"http://127.0.0.1:{port}")
        except:
            pass
        t1 = time.time()
        latencies.append((t1 - t0) * 1000)
        
    latencies.sort()
    median_latency = latencies[len(latencies)//2]
    print(f"Median API Latency: {median_latency:.2f} ms")
    
    subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Starting Benchmarks...")
measure_app("python fastapi_app/main.py", 8001, "FastAPI (Python)")
measure_app("python ../../run_vm.py aayu_app/main.aayu", 8000, "AAYU VM")
