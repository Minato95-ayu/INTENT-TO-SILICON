import shutil

import pytest

from runtime.interop.javascript import JavaScriptInteropError
from runtime.vm.vm import VirtualMachine


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is not installed")
def test_javascript_ffi_calls_node_builtin_module():
    vm = VirtualMachine()
    vm.bind_javascript_function("path", "basename", "path.basename")
    callback = vm.stdlib.registry.lookup_external("path.basename")[1]

    assert callback(["/tmp/aayu.txt"], vm) == "aayu.txt"


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is not installed")
def test_javascript_ffi_reports_node_errors():
    vm = VirtualMachine()
    vm.bind_javascript_function("path", "missingExport", "path.missingExport")

    with pytest.raises(JavaScriptInteropError, match="export is not callable"):
        vm.stdlib.registry.lookup_external("path.missingExport")[1]([], vm)