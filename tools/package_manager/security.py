import hashlib
import os

class SecurityInfo:
    @staticmethod
    def generate_checksum(filepath: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @staticmethod
    def verify_checksum(filepath: str, expected_hash: str) -> bool:
        if not os.path.exists(filepath):
            return False
        return SecurityInfo.generate_checksum(filepath) == expected_hash
