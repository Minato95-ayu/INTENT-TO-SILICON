import struct
from dataclasses import dataclass

# Magic bytes: "AAYU" in ASCII
MAGIC = b'\x41\x41\x59\x55'

@dataclass
class BinaryHeader:
    """AAYU Bytecode file header.
    
    Layout (16 bytes total):
        Offset  Size  Field
        0       4     Magic ("AAYU" = 0x41414955)
        4       1     Version Major
        5       1     Version Minor
        6       4     Instruction Count (big-endian)
        10      4     Constant Pool Size (big-endian)
        14      2     Flags (reserved)
    """
    version_major: int = 1
    version_minor: int = 0
    instruction_count: int = 0
    constant_pool_size: int = 0
    flags: int = 0

    HEADER_SIZE = 16

    def serialize(self) -> bytes:
        """Serialize header to 16 bytes."""
        return struct.pack(
            '>4sBBIIH',
            MAGIC,
            self.version_major,
            self.version_minor,
            self.instruction_count,
            self.constant_pool_size,
            self.flags
        )

    @staticmethod
    def deserialize(data: bytes) -> 'BinaryHeader':
        """Deserialize 16 bytes into a BinaryHeader."""
        if len(data) < BinaryHeader.HEADER_SIZE:
            raise ValueError(f"Header too short: {len(data)} bytes (need {BinaryHeader.HEADER_SIZE})")

        magic, major, minor, inst_count, pool_size, flags = struct.unpack(
            '>4sBBIIH', data[:BinaryHeader.HEADER_SIZE]
        )

        if magic != MAGIC:
            raise ValueError(f"Invalid magic bytes: {magic!r} (expected {MAGIC!r})")

        return BinaryHeader(
            version_major=major,
            version_minor=minor,
            instruction_count=inst_count,
            constant_pool_size=pool_size,
            flags=flags
        )

    def __repr__(self):
        return (
            f"BinaryHeader(AAYU v{self.version_major}.{self.version_minor}, "
            f"instructions={self.instruction_count}, "
            f"constants={self.constant_pool_size}, "
            f"flags=0x{self.flags:04X})"
        )
