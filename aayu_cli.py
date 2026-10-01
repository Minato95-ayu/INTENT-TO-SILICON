import sys
import os
import subprocess

def compile_aayu_to_bytecode(source_file, out_file):
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    strings = []
    bytecode = bytearray()
    
    # Very basic single-pass compiler for testing the new Native features
    for line in lines:
        line = line.strip()
        if not line or line.startswith("//"):
            continue
            
        if line.startswith("print("):
            val = line[6:-1].strip('"')
            strings.append(val)
            str_idx = len(strings) - 1
            
            # PushConst (0x01) -> but wait, string is not in constants, string is constructed
            # Let's add a new opcode 'PushString' = 0x04 in our test, 
            # OR we can just use a fake opcode 0x10 to mean PushString.
            bytecode.append(0x10) # PushString
            bytecode.extend(str_idx.to_bytes(2, 'little'))
            bytecode.append(81) # Print (81)
            
        elif line.startswith("Tensor.new"):
            bytecode.append(160) # TensorCreate
        elif line.startswith("Db.set"):
            bytecode.append(170) # DbSet
        elif line.startswith("Db.get"):
            bytecode.append(171) # DbGet
        elif line.startswith("Server.start"):
            bytecode.append(180) # ServerStart
    
    bytecode.append(0x00) # Halt
    
    with open(out_file, 'wb') as f:
        # MAGIC
        f.write(b'AAYU')
        # STRINGS COUNT
        f.write(len(strings).to_bytes(4, 'little'))
        for s in strings:
            enc = s.encode('utf-8')
            f.write(len(enc).to_bytes(4, 'little'))
            f.write(enc)
        # BYTECODE
        f.write(bytecode)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: aayu run <file.aayu>")
        sys.exit(1)
        
    cmd = sys.argv[1]
    target = sys.argv[2]
    
    if cmd == "run":
        temp_bc = target.replace(".aayu", ".aybc")
        compile_aayu_to_bytecode(target, temp_bc)
        
        rust_vm = r"D:\INTENT-TO-SILICON\runtime_rs\target\debug\aayu-vm.exe"
        subprocess.run([rust_vm, temp_bc])
        
        if os.path.exists(temp_bc):
            os.remove(temp_bc)
