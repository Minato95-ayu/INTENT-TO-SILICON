import struct

out = bytearray()
out.extend(b'AAYU')
out.extend(struct.pack("<BB", 1, 0)) # version 1.0

# Constant Pool
# We need: 10 (INT), 20 (INT)
out.extend(struct.pack("<I", 2)) # CP Size: 2

# Const 0: 10
out.append(0) # TYPE_INT
out.extend(struct.pack("<q", 10))

# Const 1: 20
out.append(0) # TYPE_INT
out.extend(struct.pack("<q", 20))

# Bytecode (OP_PUSH_CONST 0, OP_PUSH_CONST 1, OP_ADD, OP_PRINT, OP_HALT)
bytecode = bytearray()
bytecode.append(0x01) # OP_PUSH_CONST
bytecode.extend(struct.pack(">H", 0))

bytecode.append(0x01) # OP_PUSH_CONST
bytecode.extend(struct.pack(">H", 1))

bytecode.append(0x10) # OP_ADD
bytecode.extend(struct.pack(">H", 0))

bytecode.append(0x51) # OP_PRINT
bytecode.extend(struct.pack(">H", 0))

bytecode.append(0xFF) # OP_HALT
bytecode.extend(struct.pack(">H", 0))

out.extend(struct.pack("<I", len(bytecode)))
out.extend(bytecode)

with open("test_math.ayc", "wb") as f:
    f.write(out)
