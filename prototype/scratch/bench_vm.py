import time
import subprocess
import os
import statistics

# Paths
PYTHON_CLI = "cli.py"
RUST_CLI = "aayu-rs/target/release/aayu_cli.exe"

def run_cmd(args, cwd):
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
    stdout, stderr = p.communicate()
    return stdout, stderr, p.returncode

def compile_aayu(aayu_path, cwd):
    stdout, stderr, code = run_cmd(["python", PYTHON_CLI, "compile", aayu_path], cwd)
    if code != 0:
        raise Exception(f"Failed to compile {aayu_path}: {stderr}")

def run_python_vm(ayc_path, cwd):
    t_start = time.perf_counter()
    stdout, stderr, code = run_cmd(["python", PYTHON_CLI, "vm", ayc_path], cwd)
    t_end = time.perf_counter()
    if code != 0:
        raise Exception(f"Python VM failed on {ayc_path}: {stderr}")
    return stdout.strip(), (t_end - t_start) * 1000.0 # ms

def run_rust_vm(ayc_path, cwd):
    t_start = time.perf_counter()
    stdout, stderr, code = run_cmd([RUST_CLI, ayc_path], cwd)
    t_end = time.perf_counter()
    if code != 0:
        raise Exception(f"Rust VM failed on {ayc_path}: {stderr}")
    return stdout.strip(), (t_end - t_start) * 1000.0 # ms

def generate_fib_file(n):
    code = f"""task fib with n.
    if n == 0.
        return 0.
    end.
    if n == 1.
        return 1.
    end.
    number a is n - 1.
    number b is n - 2.
    number f1 is run fib with a.
    number f2 is run fib with b.
    return f1 + f2.
end.

show run fib with {n}.
"""
    path = "tests/temp_fib.aayu"
    with open(path, "w") as f:
        f.write(code)
    return path

def measure_benchmark(run_fn, path, cwd):
    # Warmup
    out_warm, t_warm = run_fn(path, cwd)
    
    # Decide iterations based on warmup time
    if t_warm > 5000.0: # > 5 seconds
        iterations = 1
    elif t_warm > 1000.0: # > 1 second
        iterations = 3
    else:
        iterations = 10
        
    times = [t_warm] # Include warmup or run separately? Actually, let's run separately to keep warmup out of metrics
    times = []
    output = None
    for _ in range(iterations):
        out, t = run_fn(path, cwd)
        times.append(t)
        output = out
        
    mean_val = statistics.mean(times)
    median_val = statistics.median(times)
    
    # Simple percentile calculation
    times_sorted = sorted(times)
    idx = int(len(times_sorted) * 0.95)
    p95_val = times_sorted[min(idx, len(times_sorted) - 1)]
    
    return output, mean_val, median_val, p95_val

def main():
    cwd = os.getcwd()
    print("AAYU Runtime Benchmarking Suite", flush=True)
    print("=============================", flush=True)
    
    fib_inputs = [20, 25, 30, 32, 35]
    reports = []
    
    print("\nStarting Fibonacci Benchmarks...", flush=True)
    for n in fib_inputs:
        print(f"Benchmarking Fib({n})...", flush=True)
        path = generate_fib_file(n)
        compile_aayu(path, cwd)
        ayc_path = path.replace(".aayu", ".ayc")
        
        # Python VM
        py_out, py_mean, py_med, py_p95 = measure_benchmark(run_python_vm, ayc_path, cwd)
        
        # Rust VM
        rs_out, rs_mean, rs_med, rs_p95 = measure_benchmark(run_rust_vm, ayc_path, cwd)
        
        # Cleanup temp files
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(ayc_path):
            os.remove(ayc_path)
        
        # Parity check
        parity = "PASS" if py_out == rs_out else f"FAIL (Py: {py_out}, Rs: {rs_out})"
        speedup = py_mean / rs_mean if rs_mean > 0 else 0
        
        reports.append({
            "name": f"Fib({n})",
            "py_result": py_out,
            "rs_result": rs_out,
            "parity": parity,
            "py_time": py_mean,
            "rs_time": rs_mean,
            "speedup": speedup,
            "py_med": py_med,
            "rs_med": rs_med,
            "py_p95": py_p95,
            "rs_p95": rs_p95
        })
        print(f"\n{reports[-1]['name']}", flush=True)
        print(f"Python Result : {py_out}", flush=True)
        print(f"Rust Result   : {rs_out}", flush=True)
        print(f"Parity        : {'PASS' if py_out == rs_out else 'FAIL'}", flush=True)
        print(f"Python Time   : {py_mean:.1f} ms", flush=True)
        print(f"Rust Time     : {rs_mean:.1f} ms", flush=True)
        print(f"Speedup       : {speedup:.1f}x", flush=True)
        
    print("\nBenchmarking Arithmetic Loop (1,000,000 iterations)...", flush=True)
    loop_path = "tests/vm_loop.aayu"
    compile_aayu(loop_path, cwd)
    loop_ayc_path = loop_path.replace(".aayu", ".ayc")
    
    # Python VM
    py_out, py_mean, py_med, py_p95 = measure_benchmark(run_python_vm, loop_ayc_path, cwd)
    
    # Rust VM
    rs_out, rs_mean, rs_med, rs_p95 = measure_benchmark(run_rust_vm, loop_ayc_path, cwd)
    
    parity = "PASS" if py_out == rs_out else f"FAIL (Py: {py_out}, Rs: {rs_out})"
    speedup = py_mean / rs_mean if rs_mean > 0 else 0
    
    reports.append({
        "name": "Arithmetic Loop",
        "py_result": py_out,
        "rs_result": rs_out,
        "parity": parity,
        "py_time": py_mean,
        "rs_time": rs_mean,
        "speedup": speedup,
        "py_med": py_med,
        "rs_med": rs_med,
        "py_p95": py_p95,
        "rs_p95": rs_p95
    })
    print(f"\n{reports[-1]['name']}", flush=True)
    print(f"Python Result : {py_out}", flush=True)
    print(f"Rust Result   : {rs_out}", flush=True)
    print(f"Parity        : {'PASS' if py_out == rs_out else 'FAIL'}", flush=True)
    print(f"Python Time   : {py_mean:.1f} ms", flush=True)
    print(f"Rust Time     : {rs_mean:.1f} ms", flush=True)
    print(f"Speedup       : {speedup:.1f}x", flush=True)
    
    # Format report
    print("\n\n", flush=True)
    print("AAYU Runtime Benchmark Report", flush=True)
    print("=============================", flush=True)
    print(f"{'Benchmark':<18} | {'Parity':<6} | {'Python Time (Mean)':<20} | {'Rust Time (Mean)':<18} | {'Speedup':<10}", flush=True)
    print("-" * 80, flush=True)
    for r in reports:
        print(f"{r['name']:<18} | {r['parity']:<6} | {r['py_time']:>15.2f} ms | {r['rs_time']:>13.2f} ms | {r['speedup']:>8.1f}x", flush=True)
        
    print("\nDetailed Metrics (Mean / Median / P95)", flush=True)
    print("-" * 80, flush=True)
    for r in reports:
        print(f"{r['name']}:", flush=True)
        print(f"  Python : Mean = {r['py_time']:.2f} ms, Median = {r['py_med']:.2f} ms, P95 = {r['py_p95']:.2f} ms", flush=True)
        print(f"  Rust   : Mean = {r['rs_time']:.2f} ms, Median = {r['rs_med']:.2f} ms, P95 = {r['rs_p95']:.2f} ms", flush=True)
        print(f"  ", flush=True)

if __name__ == "__main__":
    main()
