import struct
import sys

def dump_ayc(filepath):
    with open(filepath, 'rb') as f:
        magic = f.read(4)
        print("Magic:", magic)
        version = struct.unpack("BB", f.read(2))
        print("Version:", version)
        cp_size, = struct.unpack("<I", f.read(4))
        print("CP Size:", cp_size)
        
        for i in range(cp_size):
            type_tag = f.read(1)[0]
            if type_tag == 0: # TYPE_INT
                val, = struct.unpack("<q", f.read(8))
                print(f"Const {i}: INT {val}")
            elif type_tag == 1: # TYPE_FLOAT
                val, = struct.unpack("<d", f.read(8))
                print(f"Const {i}: FLOAT {val}")
            elif type_tag == 2 or type_tag == 3: # TYPE_STRING / DICT
                length, = struct.unpack("<I", f.read(4))
                s = f.read(length).decode('utf-8')
                print(f"Const {i}: STR/DICT '{s}'")
            elif type_tag == 4: # TYPE_BOOL
                val = f.read(1)[0]
                print(f"Const {i}: BOOL {val}")
                
        bc_size, = struct.unpack("<I", f.read(4))
        print("Bytecode Size:", bc_size)
        bc = f.read(bc_size)
        print("Bytecode:", bc.hex())

if __name__ == "__main__":
    dump_ayc(sys.argv[1])
