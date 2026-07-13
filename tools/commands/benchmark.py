import sys
from runtime.vm_next.config import VMConfig
from runtime.vm_next.vm import VirtualMachine
from runtime.vm_next.instructions import Opcode

def handle(args):
    """
    Mock Benchmark Harness for VM Validation.
    Executes a tight arithmetic loop (10M instructions).
    """
    print("AAYU Benchmark Suite")
    print("--------------------")
    print("Running Arithmetic (10M Instructions) ...")
    
    bytecode = bytearray()
    constant_pool = [1, 2] # Dummy constants
    
    print("Generating 1M bytecode payload...")
    count = 1000000
    for i in range(count // 2):
        bytecode.append(Opcode.PUSH_CONST)
        bytecode.append(0)
        bytecode.append(0)
        bytecode.append(Opcode.POP)
    bytecode.append(Opcode.HALT)
    
    vm = VirtualMachine(VMConfig.production())
    vm.load(bytecode, constant_pool)
    
    print("Executing...")
    vm.execute()
    
    summary = vm.profiler.summary()
    
    print("\n[Arithmetic]")
    print(f"Instructions: {summary['instructions']}")
    print(f"Time: {summary['time']:.2f}s")
    if summary['time'] > 0:
        ips = summary['instructions'] / summary['time']
        print(f"IPS: {ips/1000000:.1f}M/sec")
    else:
        print("IPS: N/A")
    print(f"Peak Memory: {summary['peak_memory']} bytes")
    print(f"Leaks: {len(vm.heap.allocator.pool.pool)}")
    
    print("\nBenchmark Complete.")

if __name__ == '__main__':
    handle([])
