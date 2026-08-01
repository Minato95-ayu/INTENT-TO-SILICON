import asyncio
import httpx
import time
import os
import psutil
import subprocess
import json
import statistics

TARGET_URL = "http://127.0.0.1:8000"

async def run_requests(client, method, url, count, payload=None, headers=None, concurrency=10):
    latencies = []
    sem = asyncio.Semaphore(concurrency)
    
    async def make_request():
        async with sem:
            start = time.perf_counter()
            if method == "GET":
                resp = await client.get(url, headers=headers)
            else:
                resp = await client.post(url, json=payload, headers=headers)
            end = time.perf_counter()
            if resp.status_code in (200, 201):
                latencies.append(end - start)
            return resp.status_code

    tasks = [make_request() for _ in range(count)]
    start_total = time.perf_counter()
    await asyncio.gather(*tasks)
    end_total = time.perf_counter()
    
    return latencies, (end_total - start_total)

def calculate_metrics(latencies, duration):
    if not latencies:
        return {"rps": 0, "p50": 0, "p95": 0, "p99": 0}
        
    latencies_ms = [l * 1000 for l in latencies]
    latencies_ms.sort()
    
    def get_percentile(p):
        idx = int(len(latencies_ms) * p)
        return latencies_ms[min(idx, len(latencies_ms) - 1)]
        
    return {
        "rps": len(latencies) / duration,
        "p50": get_percentile(0.50),
        "p95": get_percentile(0.95),
        "p99": get_percentile(0.99)
    }

def count_lines(directory):
    total_loc = 0
    total_files = 0
    for root, dirs, files in os.walk(directory):
        if "__pycache__" in root or ".venv" in root:
            continue
        for f in files:
            if f.endswith(".py") or f.endswith(".aayu") or f.endswith(".toml"):
                total_files += 1
                with open(os.path.join(root, f), 'r', encoding='utf-8', errors='ignore') as fp:
                    total_loc += sum(1 for line in fp if line.strip() and not line.strip().startswith('#'))
    return total_loc, total_files

async def benchmark_framework(name, command, directory):
    print(f"\n--- Benchmarking {name} ---")
    loc, files = count_lines(directory)
    print(f"LOC: {loc}, Files: {files}")
    
    start_time = time.time()
    process = subprocess.Popen(command, cwd=directory, shell=True)
    
    # Wait for startup
    startup_ms = 0
    for i in range(100):
        try:
            with httpx.Client() as client:
                client.get(f"{TARGET_URL}/health", timeout=0.1)
            startup_ms = (time.time() - start_time) * 1000
            break
        except Exception:
            time.sleep(0.1)
            
    if startup_ms == 0:
        print("Failed to start!")
        process.kill()
        return None

    print(f"Startup Time: {startup_ms:.2f} ms")
    
    p = psutil.Process(process.pid)
    idle_ram_mb = p.memory_info().rss / (1024 * 1024)
    print(f"Idle RAM: {idle_ram_mb:.2f} MB")
    
    peak_ram_mb = idle_ram_mb
    
    try:
        # Wait for port to be ready
        startup_time = 0
        boot_start = time.perf_counter()
        while True:
            try:
                start = time.perf_counter()
                async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as c:
                    r = await c.get(f"{TARGET_URL}/health", timeout=30.0)
                    if r.status_code == 200:
                        startup_time = (time.perf_counter() - start) * 1000
                        break
            except Exception:
                await asyncio.sleep(0.1)
                
            if time.perf_counter() - boot_start > 10:
                print("Server failed to start within 10s")
                break
                
        print(f"Startup Time: {startup_time:.2f} ms")
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0), limits=httpx.Limits(max_connections=1000, max_keepalive_connections=1000)) as client:
            # Get Auth Token
            auth_resp = await client.post(f"{TARGET_URL}/api/login", json={"email": "bench@test.com", "password": "password"})
            token = auth_resp.json().get("data", "")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Warmup
            print("Running Warmup (100 reqs)...")
            await run_requests(client, "GET", f"{TARGET_URL}/health", 100)
            
            print("Running GET /health Load (1000)...")
            health_lat, h_dur = await run_requests(client, "GET", f"{TARGET_URL}/health", 1000)
            health_metrics = calculate_metrics(health_lat, h_dur)
            
            print("Running POST /api/products Load (1000)...")
            post_lat, p_dur = await run_requests(client, "POST", f"{TARGET_URL}/api/products", 1000, 
                                                payload={"name": "Test", "price": 9.99, "stock": 100}, headers=headers)
            post_metrics = calculate_metrics(post_lat, p_dur)
            
            # Update peak ram periodically during load
            try:
                peak_ram_mb = max(peak_ram_mb, p.memory_info().rss / (1024 * 1024))
            except psutil.NoSuchProcess:
                pass

            print("Running GET /api/products Load (1000)...")
            get_lat, g_dur = await run_requests(client, "GET", f"{TARGET_URL}/api/products", 1000, headers=headers)
            get_metrics = calculate_metrics(get_lat, g_dur)
            
        process.kill()
        stdout, stderr = process.communicate()
        if stdout:
            print(f"STDOUT:\n{stdout.decode()}")
        if stderr:
            print(f"STDERR:\n{stderr.decode()}")
        
        return {
            "framework": name,
            "startup_ms": startup_time,
            "idle_ram_mb": idle_ram_mb,
            "peak_ram_mb": peak_ram_mb,
            "loc": loc,
            "files": files,
            "health_overhead": health_metrics,
            "rps_get": get_metrics["rps"],
            "rps_post": post_metrics["rps"],
            "latency_get": {
                "p50": get_metrics["p50"],
                "p95": get_metrics["p95"],
                "p99": get_metrics["p99"]
            },
            "latency_post": {
                "p50": post_metrics["p50"],
                "p95": post_metrics["p95"],
                "p99": post_metrics["p99"]
            }
        }
    except Exception as e:
        print(f"Terminating {name} server...")
        process.kill()
        stdout, stderr = process.communicate()
        if stdout:
            print(f"STDOUT:\n{stdout.decode()}")
        if stderr:
            print(f"STDERR:\n{stderr.decode()}")
        raise e

async def main():
    results = []
    
    # Run AAYU
    aayu_res = await benchmark_framework("AAYU", "python ../../aayu/cli.py run", "aayu_app")
    if aayu_res: results.append(aayu_res)
    
    # Run FastAPI
    fastapi_res = await benchmark_framework("FastAPI", "uvicorn main:app --port 8000 --workers 1", "fastapi_app")
    if fastapi_res: results.append(fastapi_res)
    
    # Run Django
    django_res = await benchmark_framework("Django", "python manage.py runserver 0.0.0.0:8000 --noreload", "django_app_project")
    if django_res: results.append(django_res)
    
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nBenchmark Complete! Results saved to results.json")

if __name__ == "__main__":
    asyncio.run(main())
