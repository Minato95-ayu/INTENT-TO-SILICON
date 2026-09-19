# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

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
