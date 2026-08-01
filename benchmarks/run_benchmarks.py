import os
import time
import subprocess
import requests
import psutil
from concurrent.futures import ThreadPoolExecutor
import random

APPS = {
    'FastAPI': {
        'cmd': ['uvicorn', 'main:app', '--port', '8000'],
        'cwd': 'benchmarks/apps/fastapi',
        'loc_file': 'benchmarks/apps/fastapi/main.py'
    },
    'Django': {
        'cmd': ['python', 'main.py', 'runserver', '8000', '--noreload'],
        'cwd': 'benchmarks/apps/django',
        'loc_file': 'benchmarks/apps/django/main.py'
    }
}

def count_loc(filepath):
    with open(filepath, 'r') as f:
        return len([line for line in f if line.strip() and not line.strip().startswith('#')])

def wait_for_server():
    for _ in range(50):
        try:
            r = requests.get('http://127.0.0.1:8000/', timeout=0.1)
            if r.status_code == 200:
                return True
        except:
            time.sleep(0.1)
    return False

def benchmark_latency_rps():
    for _ in range(10):
        try:
            requests.get('http://127.0.0.1:8000/items/42')
        except:
            pass
    start = time.time()
    reqs = 500
    def fetch():
        requests.get('http://127.0.0.1:8000/items/42')
    with ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(reqs):
            executor.submit(fetch)
    end = time.time()
    duration = end - start
    rps = reqs / duration
    latency = (duration / reqs) * 1000 # ms
    return rps, latency

def run_benchmarks():
    print("# Web Framework Benchmark: AAYU vs FastAPI vs Django")
    print("| Framework | LOC | Startup Time (s) | RAM (MB) | RPS | Avg Latency (ms) |")
    print("|-----------|-----|------------------|----------|-----|------------------|")

    for name, config in APPS.items():
        loc = count_loc(config['loc_file'])
        cwd = config.get('cwd', os.getcwd())
        start_time = time.time()
        proc = subprocess.Popen(config['cmd'], cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ready = wait_for_server()
        startup_time = time.time() - start_time
        if not ready:
            proc.kill()
            continue
        try:
            process = psutil.Process(proc.pid)
            mem_mb = process.memory_info().rss / (1024 * 1024)
            for child in process.children(recursive=True):
                mem_mb += child.memory_info().rss / (1024 * 1024)
        except:
            mem_mb = 0
        rps, latency = benchmark_latency_rps()
        proc.kill()
        proc.wait()
        print(f"| {name} | {loc} | {startup_time:.3f} | {mem_mb:.1f} | {rps:.1f} | {latency:.2f} |")
        time.sleep(1)


if __name__ == '__main__':
    run_benchmarks()
