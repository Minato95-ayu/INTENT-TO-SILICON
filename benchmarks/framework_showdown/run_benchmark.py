import subprocess
import time
import psutil
import requests
import os
import signal
import statistics
import json
import socket

def get_directory_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def measure_app(command, port, name, app_dir_size_mb, setup_script=None):
    print(f"\n[{name}] Measuring Cold Boot & Startup Memory")
    
    if is_port_in_use(port):
        print(f"Port {port} is already in use. Skipping.")
        return None
        
    start_time = time.time()
    process = subprocess.Popen(command, shell=True)
    
    # Wait for startup
    startup_time = 0
    while True:
        try:
            requests.get(f"http://127.0.0.1:{port}/api/products", timeout=1)
            startup_time = (time.time() - start_time) * 1000
            break
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
            time.sleep(0.01)
            if time.time() - start_time > 10:
                print(f"Failed to start {name}")
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return None
                
    time.sleep(1) # Let it settle
    
    # Measure Idle Memory
    p = psutil.Process(process.pid)
    memory_mb = p.memory_info().rss / (1024 * 1024)
    
    print(f"Startup Time: {startup_time:.2f} ms")
    print(f"Idle Memory: {memory_mb:.2f} MB")
    
    # Measure Latency (30 runs)
    print(f"[{name}] Running Latency Benchmark (30 runs)")
    latencies = []
    for _ in range(30):
        t0 = time.time()
        try:
            requests.get(f"http://127.0.0.1:{port}/api/products", timeout=1)
        except:
            pass
        t1 = time.time()
        latencies.append((t1 - t0) * 1000)
        
    median_latency = statistics.median(latencies)
    min_latency = min(latencies)
    max_latency = max(latencies)
    std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0
    
    print(f"Median: {median_latency:.2f} ms | Min: {min_latency:.2f} | Max: {max_latency:.2f} | StdDev: {std_dev:.2f}")
    
    subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2) # Cooldown
    
    return {
        "framework": name,
        "dependency_size_mb": app_dir_size_mb,
        "startup_time_ms": round(startup_time, 2),
        "memory_mb": round(memory_mb, 2),
        "latency_ms": {
            "median": round(median_latency, 2),
            "min": round(min_latency, 2),
            "max": round(max_latency, 2),
            "std_dev": round(std_dev, 2)
        }
    }

def run_all():
    print("=== FRAMEWORK SHOWDOWN METRICS ===")
    results = []
    
    # Size calculation for AAYU (Full compiler/runtime size)
    aayu_size = (get_directory_size("../../compiler") + get_directory_size("../../runtime")) / (1024*1024)
    
    # Approx sizes in standard venvs for these frameworks
    fastapi_venv_size = 48.5 # MB
    django_venv_size = 62.3 # MB
    
    res_aayu = measure_app("python ../../run_vm.py aayu_app/main.aayu", 8000, "AAYU VM", aayu_size)
    if res_aayu: results.append(res_aayu)
    
    res_fastapi = measure_app("python fastapi_app/main.py", 8001, "FastAPI", fastapi_venv_size)
    if res_fastapi: results.append(res_fastapi)
    
    # Run django app
    res_django = measure_app("python django_app/manage.py runserver 8002", 8002, "Django REST", django_venv_size)
    if res_django: results.append(res_django)
    
    with open("performance_report.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("\nBenchmark saved to performance_report.json")

if __name__ == "__main__":
    run_all()
