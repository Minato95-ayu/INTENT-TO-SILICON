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

from ..registry import StdLibRegistry
from ...values.boolean import BooleanValue

def register_testing_lib(registry: StdLibRegistry):
    def fn_assert_eq(args, vm):
        v1 = args[0]
        v2 = args[1]
        
        # Proper deep comparison
        if hasattr(v1, 'to_python') and hasattr(v2, 'to_python'):
            if v1.to_python() == v2.to_python():
                return BooleanValue(True)
        elif hasattr(v1, 'value') and hasattr(v2, 'value'):
            if v1.value == v2.value:
                return BooleanValue(True)
                
        return BooleanValue(False)
        
    registry.register("testing::assert_eq", fn_assert_eq)
