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

import re
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.boolean import BooleanValue

def register_regex_lib(registry: StdLibRegistry):
    def fn_match(args, vm):
        try:
            pattern = args[0].to_python()
            string = args[1].to_python()
            return BooleanValue(bool(re.match(pattern, string)))
        except Exception:
            return BooleanValue(False)
            
    registry.register("regex::match", fn_match)
