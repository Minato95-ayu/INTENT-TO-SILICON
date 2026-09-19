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

import ctypes.util

import pytest

from runtime.interop.native import NativeInteropError
from runtime.vm.vm import VirtualMachine


def test_native_ffi_binds_c_strlen_when_available():
    library = ctypes.util.find_library("c") or ctypes.util.find_library("msvcrt")
    if not library:
        pytest.skip("No platform C runtime library found")

    vm = VirtualMachine()
    vm.bind_native_function(
        library,
        "strlen",
        "libc.strlen",
        "Int",
        ["String"],
    )
    callback = vm.stdlib.registry.lookup_external("libc.strlen")[1]

    assert callback(["AAYU"], vm) == 4


def test_native_ffi_rejects_unsupported_types():
    with pytest.raises(NativeInteropError, match="Unsupported native ABI type"):
        from runtime.interop.native import _resolve_type

        _resolve_type("List")