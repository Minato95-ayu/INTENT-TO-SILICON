import pytest
from runtime.ui.runtime import UIRuntime

def test_ui_runtime_e2e():
    rt = UIRuntime({})
    rt.initialize()
    # It initializes correctly without throwing errors
    assert rt is not None
    # Check if adapter is present
    assert rt.adapter is not None
