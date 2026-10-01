import sys
import os
import subprocess
import re

def compile_aayu_to_bytecode(source_file, out_file):
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    strings = []
    bytecode = bytearray()
    
    def get_string_idx(val):
        if val not in strings:
            strings.append(val)
        return strings.index(val)

    for line in lines:
        line = line.strip()
        if not line or line.startswith("//"):
            continue
            
        # Ignore import statements (handled virtually for now)
        if line.startswith("import "):
            continue
            
        # PRINT statement
        print_match = re.match(r'print\("(.*?)"\)', line)
        if print_match:
            val = print_match.group(1)
            idx = get_string_idx(val)
            bytecode.append(0x10) # PushString
            bytecode.extend(idx.to_bytes(2, 'little'))
            bytecode.append(81) # Print
            continue

        # DB operations
        db_set_match = re.match(r'Db\.set\("(.*?)",\s*"(.*?)"\)', line)
        if db_set_match:
            k, v = db_set_match.groups()
            idx_k = get_string_idx(k)
            idx_v = get_string_idx(v)
            
            bytecode.append(0x10) # PushString (Key)
            bytecode.extend(idx_k.to_bytes(2, 'little'))
            
            bytecode.append(0x10) # PushString (Value)
            bytecode.extend(idx_v.to_bytes(2, 'little'))
            
            bytecode.append(170) # DbSet
            continue
            
        db_get_match = re.match(r'Db\.get\("(.*?)"\)', line)
        if db_get_match:
            k = db_get_match.group(1)
            idx_k = get_string_idx(k)
            bytecode.append(0x10) # PushString (Key)
            bytecode.extend(idx_k.to_bytes(2, 'little'))
            bytecode.append(171) # DbGet
            # Print the retrieved value natively for testing
            bytecode.append(81) # Print
            continue

        # SERVER operations
        srv_match = re.match(r'Server\.start\((\d+)\)', line)
        if srv_match:
            port = int(srv_match.group(1))
            # PushConst port
            # For simplicity, we just trigger ServerStart (180) which mocks port 3000 in Rust for now
            bytecode.append(180)
            continue
            
        # TENSOR operations
        tensor_match = re.match(r'Tensor\.new\(.*?\)', line)
        if tensor_match:
            bytecode.append(160)
            continue
            
        # UI operations
        ui_render = re.match(r'UI\.render\("(.*?)"\)', line)
        if ui_render:
            val = ui_render.group(1)
            idx = get_string_idx(val)
            bytecode.append(0x10) # PushString
            bytecode.extend(idx.to_bytes(2, 'little'))
            bytecode.append(190) # UIRender
            continue

    bytecode.append(0x00) # Halt
    
    with open(out_file, 'wb') as f:
        f.write(b'AAYU')
        f.write(len(strings).to_bytes(4, 'little'))
        for s in strings:
            enc = s.encode('utf-8')
            f.write(len(enc).to_bytes(4, 'little'))
            f.write(enc)
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
        if not os.path.exists(rust_vm):
            print("Error: Rust VM not found at", rust_vm)
            sys.exit(1)
            
        subprocess.run([rust_vm, temp_bc])
        
        if os.path.exists(temp_bc):
            os.remove(temp_bc)
