import sys
import time
import threading
import urllib.request
import urllib.error

def run_loadtest(url, concurrency, duration):
    print(f"Starting load test on {url} with concurrency {concurrency} for {duration} seconds.")
    
    stop_flag = False
    stats = {"reqs": 0, "success": 0, "errors": 0}
    lock = threading.Lock()
    
    def worker():
        while not stop_flag:
            try:
                start = time.time()
                with urllib.request.urlopen(url, timeout=2) as response:
                    response.read()
                
                with lock:
                    stats["reqs"] += 1
                    stats["success"] += 1
            except Exception as e:
                with lock:
                    stats["reqs"] += 1
                    stats["errors"] += 1

    threads = []
    for _ in range(concurrency):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads.append(t)
        
    time.sleep(duration)
    stop_flag = True
    
    for t in threads:
        t.join(timeout=1.0)
        
    print("\n--- Load Test Results ---")
    print(f"Total Requests: {stats['reqs']}")
    print(f"Successful: {stats['success']}")
    print(f"Errors: {stats['errors']}")
    print(f"Requests/sec: {stats['reqs'] / duration:.2f}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python loadtest.py <url> <concurrency> <duration_sec>")
        sys.exit(1)
        
    run_loadtest(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
