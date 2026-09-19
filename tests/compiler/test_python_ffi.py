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

import pytest

from runtime.interop.python import PythonInteropError
from runtime.vm.vm import VirtualMachine


def test_python_ffi_binds_standard_library_function():
    vm = VirtualMachine()
    vm.bind_python_function("math", "sqrt", "math.sqrt")
    callback = vm.stdlib.registry.lookup_external("math.sqrt")[1]

    assert callback([81], vm) == 9


def test_python_ffi_reports_missing_function():
    vm = VirtualMachine()
    with pytest.raises(PythonInteropError, match="Unable to bind Python function"):
        vm.bind_python_function("math", "missing_function", "math.missing")