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