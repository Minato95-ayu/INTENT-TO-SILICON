"""
=============================================================================
FILE: stress_test.py
PURPOSE: Test file - Validates system functionality
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test file - validates system functionality.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import sys
import time
import threading
import gc
import json
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil

# Ensure prototype root is in PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "aayu_language"))

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from vm import VirtualMachine

PORT = 8085
BASE_URL = f"http://localhost:{PORT}"

def cleanup_db():
    db_path = "aayu_db.sqlite"
    for suffix in ["", "-wal", "-journal", "-shm"]:
        path = db_path + suffix
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

def compile_and_start_server():
    cleanup_db()
    
    filepath = os.path.join(os.path.dirname(__file__), "vm_web_route.aayu")
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
        
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize(), filename=filepath)
    ast = parser.parse()
    
    compiler = AAYUCompiler()
    bytecode = compiler.compile(ast)
    
    vm = VirtualMachine()
    vm.run(bytecode)
    
    server_thread = threading.Thread(
        target=vm.globals["http_serve"],
        args=(PORT,)
    )
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to boot
    time.sleep(1.0)
    return vm

def get_stats():
    gc.collect()
    process = psutil.Process(os.getpid())
    return {
        "rss": process.memory_info().rss / (1024 * 1024), # MB
        "gc_objects": len(gc.get_objects()),
        "threads": threading.active_count()
    }

def run_get_load(num_requests, max_workers=50):
    latencies = []
    success_count = 0
    failed_count = 0
    sqlite_locks = 0
    vm_exceptions = 0
    
    t_total_list = []
    t_db_wait_list = []
    t_db_exec_list = []
    t_template_list = []
    t_vm_list = []
    t_residual_list = []
    
    start_time = time.perf_counter()
    
    def single_request():
        nonlocal success_count, failed_count, sqlite_locks, vm_exceptions
        req_start = time.perf_counter()
        try:
            req = urllib.request.Request(f"{BASE_URL}/books", method="GET")
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    resp.read() # Consume response body
                    success_count += 1
                    
                    # Expose profiling headers
                    h_total = float(resp.headers.get("X-Profiling-Total", 0.0))
                    h_wait = float(resp.headers.get("X-Profiling-Db-Wait", 0.0))
                    h_exec = float(resp.headers.get("X-Profiling-Db-Exec", 0.0))
                    h_temp = float(resp.headers.get("X-Profiling-Template", 0.0))
                    h_vm = float(resp.headers.get("X-Profiling-Vm", 0.0))
                    
                    h_resid = max(0.0, h_vm - (h_wait + h_exec + h_temp))
                    
                    t_total_list.append(h_total)
                    t_db_wait_list.append(h_wait)
                    t_db_exec_list.append(h_exec)
                    t_template_list.append(h_temp)
                    t_vm_list.append(h_vm)
                    t_residual_list.append(h_resid)
                else:
                    failed_count += 1
        except urllib.error.HTTPError as e:
            failed_count += 1
            body = e.read().decode('utf-8', errors='ignore')
            print(f"DEBUG GET HTTPError {e.code}: {body}")
            if "locked" in body.lower():
                sqlite_locks += 1
            else:
                vm_exceptions += 1
        except Exception as e:
            failed_count += 1
            print(f"DEBUG GET Exception: {type(e).__name__}: {str(e)}")
            vm_exceptions += 1
        finally:
            req_end = time.perf_counter()
            latencies.append((req_end - req_start) * 1000) # ms
            
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(single_request) for _ in range(num_requests)]
        for f in as_completed(futures):
            pass
            
    total_time = time.perf_counter() - start_time
    rps = num_requests / total_time if total_time > 0 else 0
    latencies.sort()
    
    def get_list_stats(lst):
        if not lst:
            return {"avg": 0.0, "p95": 0.0, "p99": 0.0}
        sorted_lst = sorted(lst)
        return {
            "avg": sum(sorted_lst) / len(sorted_lst),
            "p95": sorted_lst[int(len(sorted_lst) * 0.95)] if len(sorted_lst) > 0 else 0.0,
            "p99": sorted_lst[int(len(sorted_lst) * 0.99)] if len(sorted_lst) > 0 else 0.0
        }
    
    return {
        "success": success_count,
        "failed": failed_count,
        "sqlite_locks": sqlite_locks,
        "vm_exceptions": vm_exceptions,
        "rps": rps,
        "avg": sum(latencies) / len(latencies) if latencies else 0,
        "p95": latencies[int(len(latencies) * 0.95)] if latencies else 0,
        "p99": latencies[int(len(latencies) * 0.99)] if latencies else 0,
        "t_total": get_list_stats(t_total_list),
        "t_db_wait": get_list_stats(t_db_wait_list),
        "t_db_exec": get_list_stats(t_db_exec_list),
        "t_template": get_list_stats(t_template_list),
        "t_vm": get_list_stats(t_vm_list),
        "t_residual": get_list_stats(t_residual_list)
    }

def run_post_load(num_requests):
    latencies = []
    success_count = 0
    failed_count = 0
    sqlite_locks = 0
    vm_exceptions = 0
    
    t_total_list = []
    t_db_wait_list = []
    t_db_exec_list = []
    t_template_list = []
    t_vm_list = []
    t_residual_list = []
    
    barrier = threading.Barrier(num_requests)
    
    def worker(i):
        nonlocal success_count, failed_count, sqlite_locks, vm_exceptions
        # Wait for all threads to align before starting
        barrier.wait()
        
        req_start = time.perf_counter()
        post_data = urllib.parse.urlencode({"title": f"Book_{i}"}).encode('utf-8')
        try:
            req = urllib.request.Request(f"{BASE_URL}/add", data=post_data, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    resp.read() # Consume response
                    success_count += 1
                    
                    # Expose profiling headers
                    h_total = float(resp.headers.get("X-Profiling-Total", 0.0))
                    h_wait = float(resp.headers.get("X-Profiling-Db-Wait", 0.0))
                    h_exec = float(resp.headers.get("X-Profiling-Db-Exec", 0.0))
                    h_temp = float(resp.headers.get("X-Profiling-Template", 0.0))
                    h_vm = float(resp.headers.get("X-Profiling-Vm", 0.0))
                    
                    h_resid = max(0.0, h_vm - (h_wait + h_exec + h_temp))
                    
                    t_total_list.append(h_total)
                    t_db_wait_list.append(h_wait)
                    t_db_exec_list.append(h_exec)
                    t_template_list.append(h_temp)
                    t_vm_list.append(h_vm)
                    t_residual_list.append(h_resid)
                else:
                    failed_count += 1
        except urllib.error.HTTPError as e:
            failed_count += 1
            body = e.read().decode('utf-8', errors='ignore')
            print(f"DEBUG POST HTTPError {e.code}: {body}")
            if "locked" in body.lower():
                sqlite_locks += 1
            else:
                vm_exceptions += 1
        except Exception as e:
            failed_count += 1
            print(f"DEBUG POST Exception: {type(e).__name__}: {str(e)}")
            vm_exceptions += 1
        finally:
            req_end = time.perf_counter()
            latencies.append((req_end - req_start) * 1000) # ms
            
    threads = []
    for i in range(num_requests):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    latencies.sort()
    
    def get_list_stats(lst):
        if not lst:
            return {"avg": 0.0, "p95": 0.0, "p99": 0.0}
        sorted_lst = sorted(lst)
        return {
            "avg": sum(sorted_lst) / len(sorted_lst),
            "p95": sorted_lst[int(len(sorted_lst) * 0.95)] if len(sorted_lst) > 0 else 0.0,
            "p99": sorted_lst[int(len(sorted_lst) * 0.99)] if len(sorted_lst) > 0 else 0.0
        }
        
    return {
        "success": success_count,
        "failed": failed_count,
        "sqlite_locks": sqlite_locks,
        "vm_exceptions": vm_exceptions,
        "avg": sum(latencies) / len(latencies) if latencies else 0,
        "p95": latencies[int(len(latencies) * 0.95)] if latencies else 0,
        "p99": latencies[int(len(latencies) * 0.99)] if latencies else 0,
        "t_total": get_list_stats(t_total_list),
        "t_db_wait": get_list_stats(t_db_wait_list),
        "t_db_exec": get_list_stats(t_db_exec_list),
        "t_template": get_list_stats(t_template_list),
        "t_vm": get_list_stats(t_vm_list),
        "t_residual": get_list_stats(t_residual_list)
    }


def main():
    print("Initializing AAYU Web Runtime for Stress Testing...")
    vm = compile_and_start_server()
    
    # Environment info
    import platform
    py_ver = platform.python_version()
    os_name = platform.system() + " " + platform.release()
    cpu_info = platform.processor()
    
    print("\n==========================\n")
    print("AAYU Runtime Stress Report")
    print("==========================\n")
    print("Environment")
    print("------------")
    print(f"Python Version: {py_ver}")
    print(f"OS: {os_name}")
    print(f"CPU: {cpu_info}")
    print()
    
    # Warmup Phase (10 requests)
    print("Warmup")
    print("-------")
    print("10 Requests")
    warmup_res = run_get_load(10, max_workers=2)
    print(f"Success: {warmup_res['success']}")
    print()
    
    # Baseline stats after warmup
    baseline = get_stats()
    
    loads = [100, 250, 500, 1000]
    results = {}
    
    for load in loads:
        print(f"{load} Requests")
        print("-" * (len(str(load)) + 9))
        
        res = run_get_load(load, max_workers=50)
        post_stats = get_stats()
        
        mem_delta = post_stats["rss"] - baseline["rss"]
        gc_delta = post_stats["gc_objects"] - baseline["gc_objects"]
        
        print(f"Success: {res['success']}")
        print(f"Failed: {res['failed']}")
        print(f"RPS: {res['rps']:.1f}")
        print(f"Avg: {res['avg']:.1f}ms")
        print(f"P95: {res['p95']:.1f}ms")
        print(f"P99: {res['p99']:.1f}ms")
        print(f"Memory Delta: {mem_delta:+.3f} MB")
        print(f"GC Delta: {gc_delta:+d} objects")
        print("Latency Breakdown (Avg / P95 / P99):")
        print(f"  Total Request:    {res['t_total']['avg']:.1f}ms / {res['t_total']['p95']:.1f}ms / {res['t_total']['p99']:.1f}ms")
        print(f"  DB Lock Wait:     {res['t_db_wait']['avg']:.1f}ms / {res['t_db_wait']['p95']:.1f}ms / {res['t_db_wait']['p99']:.1f}ms")
        print(f"  DB Execution:     {res['t_db_exec']['avg']:.1f}ms / {res['t_db_exec']['p95']:.1f}ms / {res['t_db_exec']['p99']:.1f}ms")
        print(f"  Template Render:  {res['t_template']['avg']:.1f}ms / {res['t_template']['p95']:.1f}ms / {res['t_template']['p99']:.1f}ms")
        print(f"  VM Execution:     {res['t_vm']['avg']:.1f}ms / {res['t_vm']['p95']:.1f}ms / {res['t_vm']['p99']:.1f}ms")
        print(f"  Runtime Overhead: {res['t_residual']['avg']:.1f}ms / {res['t_residual']['p95']:.1f}ms / {res['t_residual']['p99']:.1f}ms")
        print()
        
        results[load] = {
            "success": res["success"],
            "failed": res["failed"],
            "mem_delta": mem_delta,
            "gc_delta": gc_delta
        }
        
    # Concurrent Writes (50)
    print("Concurrent Writes (50)")
    print("----------------------")
    write_50 = run_post_load(50)
    print(f"Success: {write_50['success']}")
    print(f"Failed: {write_50['failed']}")
    print(f"SQLite Locks: {write_50['sqlite_locks']}")
    print("Latency Breakdown (Avg / P95 / P99):")
    print(f"  Total Request:    {write_50['t_total']['avg']:.1f}ms / {write_50['t_total']['p95']:.1f}ms / {write_50['t_total']['p99']:.1f}ms")
    print(f"  DB Lock Wait:     {write_50['t_db_wait']['avg']:.1f}ms / {write_50['t_db_wait']['p95']:.1f}ms / {write_50['t_db_wait']['p99']:.1f}ms")
    print(f"  DB Execution:     {write_50['t_db_exec']['avg']:.1f}ms / {write_50['t_db_exec']['p95']:.1f}ms / {write_50['t_db_exec']['p99']:.1f}ms")
    print(f"  Template Render:  {write_50['t_template']['avg']:.1f}ms / {write_50['t_template']['p95']:.1f}ms / {write_50['t_template']['p99']:.1f}ms")
    print(f"  VM Execution:     {write_50['t_vm']['avg']:.1f}ms / {write_50['t_vm']['p95']:.1f}ms / {write_50['t_vm']['p99']:.1f}ms")
    print(f"  Runtime Overhead: {write_50['t_residual']['avg']:.1f}ms / {write_50['t_residual']['p95']:.1f}ms / {write_50['t_residual']['p99']:.1f}ms")
    print()
    
    # Concurrent Writes (100)
    print("Concurrent Writes (100)")
    print("-----------------------")
    write_100 = run_post_load(100)
    print(f"Success: {write_100['success']}")
    print(f"Failed: {write_100['failed']}")
    print(f"SQLite Locks: {write_100['sqlite_locks']}")
    print("Latency Breakdown (Avg / P95 / P99):")
    print(f"  Total Request:    {write_100['t_total']['avg']:.1f}ms / {write_100['t_total']['p95']:.1f}ms / {write_100['t_total']['p99']:.1f}ms")
    print(f"  DB Lock Wait:     {write_100['t_db_wait']['avg']:.1f}ms / {write_100['t_db_wait']['p95']:.1f}ms / {write_100['t_db_wait']['p99']:.1f}ms")
    print(f"  DB Execution:     {write_100['t_db_exec']['avg']:.1f}ms / {write_100['t_db_exec']['p95']:.1f}ms / {write_100['t_db_exec']['p99']:.1f}ms")
    print(f"  Template Render:  {write_100['t_template']['avg']:.1f}ms / {write_100['t_template']['p95']:.1f}ms / {write_100['t_template']['p99']:.1f}ms")
    print(f"  VM Execution:     {write_100['t_vm']['avg']:.1f}ms / {write_100['t_vm']['p95']:.1f}ms / {write_100['t_vm']['p99']:.1f}ms")
    print(f"  Runtime Overhead: {write_100['t_residual']['avg']:.1f}ms / {write_100['t_residual']['p95']:.1f}ms / {write_100['t_residual']['p99']:.1f}ms")
    print()
    
    # Exit Criteria Verification
    print("Exit Criteria Verification")
    print("--------------------------")
    
    # 1. 1000 Requests Success Rate >= 99%
    success_rate_1000 = (results[1000]["success"] / 1000) * 100
    p1 = success_rate_1000 >= 99.0
    p1_str = "PASS" if p1 else "FAIL"
    print(f"1000 Requests Success Rate >= 99%: {p1_str} ({success_rate_1000:.1f}%)")
    
    # 2. 50 Concurrent Writes: 0 SQLite Lock Errors
    p2 = write_50["sqlite_locks"] == 0
    p2_str = "PASS" if p2 else "FAIL"
    print(f"50 Concurrent Writes 0 SQLite Locks: {p2_str} ({write_50['sqlite_locks']} locks)")
    
    # 3. 100 Concurrent Writes: 0 SQLite Lock Errors
    p3 = write_100["sqlite_locks"] == 0
    p3_str = "PASS" if p3 else "FAIL"
    print(f"100 Concurrent Writes 0 SQLite Locks: {p3_str} ({write_100['sqlite_locks']} locks)")
    
    # 4. Memory Growth < 10 MB
    final_stats = get_stats()
    total_mem_growth = final_stats["rss"] - baseline["rss"]
    p4 = total_mem_growth < 10.0
    p4_str = "PASS" if p4 else "FAIL"
    print(f"Memory Growth < 10 MB: {p4_str} ({total_mem_growth:+.3f} MB)")
    
    # 5. VM Crashes & Deadlocks
    p5 = (results[1000]["failed"] == 0) and (write_100["failed"] == 0)
    p5_str = "PASS" if p5 else "FAIL"
    print(f"No VM Crashes / Deadlocks: {p5_str}")
    
    all_pass = p1 and p2 and p3 and p4 and p5
    print("\n--------------------------")
    if all_pass:
        print("ALL TESTS PASSED SUCCESSFULLY! Stable Runtime Candidate achieved. [OK]")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED! Needs optimization. [FAIL]")
        sys.exit(1)

if __name__ == "__main__":
    main()
