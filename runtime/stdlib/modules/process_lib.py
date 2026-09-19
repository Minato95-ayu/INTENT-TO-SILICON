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

import subprocess
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.null import NullValue

def create_string(vm, text):
    obj = vm.heap.allocate("string", text)
    return StringValue(obj, vm.heap)

def register_process_lib(registry: StdLibRegistry):
    def fn_exec(args, vm):
        try:
            cmd = args[0].to_python()
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return create_string(vm, result.stdout)
        except Exception:
            return NullValue()
            
    registry.register("process::exec", fn_exec)


