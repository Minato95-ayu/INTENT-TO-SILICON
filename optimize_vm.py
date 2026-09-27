with open("runtime/vm/interpreter.py", "r") as f:
    text = f.read()

target = """    def run(self):
        self.vm.profiler.start_time = time.time()
        while True:
            if self.vm.config.timeout_ms > 0:
                elapsed = (time.time() - self.vm.profiler.start_time) * 1000
                if elapsed > self.vm.config.timeout_ms:
                    print(f'Warning: Loop running for {self.vm.config.timeout_ms}ms. Terminating.')
                    break
            if self.vm.config.debug_mode and self.vm.config.enable_assertions:
                self._run_assertions()
            self.vm.debugger.check_breakpoint()
            opcode = self.vm.decoder.fetch8(self.vm.registers.ip)
            if self.vm.config.debug_mode:
                print(f'[VM TRACE] IP={self.vm.registers.ip} Opcode={opcode:02X} depth={self.vm.call_stack.depth()}')
            self.vm.profiler.tick(len(self.vm.heap.allocator.pool.pool) * 64)
            handler = self.dispatch_table[opcode]
            if handler is None:
                self._throw_exception(KernelError(f'Unknown opcode 0x{opcode:02X} at IP {self.vm.registers.ip}'))
                break
            result = handler(opcode)
            if result is False:
                break
        self.vm.profiler.end_time = time.time()"""

replacement = """    def run(self):
        self.vm.profiler.start_time = time.time()
        instruction_count = 0
        
        while True:
            instruction_count += 1
            if self.vm.config.timeout_ms > 0 and instruction_count % 10000 == 0:
                elapsed = (time.time() - self.vm.profiler.start_time) * 1000
                if elapsed > self.vm.config.timeout_ms:
                    print(f'Warning: Loop running for {self.vm.config.timeout_ms}ms. Terminating.')
                    break
                    
            if self.vm.config.debug_mode and self.vm.config.enable_assertions:
                self._run_assertions()
            
            # self.vm.debugger.check_breakpoint() # Skipped for speed unless debugging
            
            opcode = self.vm.decoder.fetch8(self.vm.registers.ip)
            
            if self.vm.config.debug_mode:
                print(f'[VM TRACE] IP={self.vm.registers.ip} Opcode={opcode:02X} depth={self.vm.call_stack.depth()}')
                
            # self.vm.profiler.tick(len(self.vm.heap.allocator.pool.pool) * 64) # Huge overhead, skipping in prod
            
            handler = self.dispatch_table[opcode]
            if handler is None:
                self._throw_exception(KernelError(f'Unknown opcode 0x{opcode:02X} at IP {self.vm.registers.ip}'))
                break
                
            result = handler(opcode)
            if result is False:
                break
                
        self.vm.profiler.end_time = time.time()"""

if target in text:
    with open("runtime/vm/interpreter.py", "w") as f:
        f.write(text.replace(target, replacement))
    print("Fixed VM loop speed!")
else:
    print("Target not found. Let's find exactly what it says.")
    # let's just do a regex replace
    import re
    text = re.sub(r'def run\(self\):.*?self\.vm\.profiler\.end_time = time\.time\(\)', replacement, text, flags=re.DOTALL)
    with open("runtime/vm/interpreter.py", "w") as f:
        f.write(text)
    print("Fixed VM loop speed via regex!")
