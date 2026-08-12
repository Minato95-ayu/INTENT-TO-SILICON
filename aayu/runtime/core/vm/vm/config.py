import dataclasses

@dataclasses.dataclass
class VMConfig:
    """Configuration settings for the Virtual Machine."""
    debug_mode: bool = False
    max_call_depth: int = 4096
    timeout_ms: int = -1  # -1 means no timeout (or default warning only)
    enable_assertions: bool = False
    
    @classmethod
    def development(cls):
        return cls(debug_mode=True, enable_assertions=True, timeout_ms=5000)
        
    @classmethod
    def production(cls, timeout_ms=30000):
        return cls(debug_mode=False, enable_assertions=False, timeout_ms=timeout_ms)
