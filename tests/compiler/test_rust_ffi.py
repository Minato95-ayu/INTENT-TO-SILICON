import ctypes.util

import pytest

from runtime.vm.vm import VirtualMachine


def test_rust_ffi_uses_stable_c_abi_boundary():
    library = ctypes.util.find_library("c") or ctypes.util.find_library("msvcrt")
    if not library:
        pytest.skip("No platform C runtime library found")

    vm = VirtualMachine()
    vm.bind_rust_function(library, "strlen", "rust.text_length", "Int", ["String"])
    provider, callback = vm.stdlib.registry.lookup_external("rust.text_length")

    assert provider == "rust"
    assert callback(["AAYU"], vm) == 4