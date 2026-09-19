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

from runtime.vm.instructions import Opcode
from runtime.vm.vm import VirtualMachine


def test_native_external_callback_executes_through_vm_registry():
    vm = VirtualMachine()
    vm.register_external("sqlite.open", "native", lambda args, runtime: f"opened:{args[0]}")

    assert vm.stdlib.registry.lookup_external("sqlite.open")[0] == "native"
    assert vm.stdlib.registry.lookup_external("sqlite.open")[1](["app.db"], vm) == "opened:app.db"


def test_non_native_external_callback_is_rejected_until_adapter_exists():
    vm = VirtualMachine()

    with pytest.raises(ValueError, match="only native callbacks are supported"):
        vm.register_external("numpy.array", "python", lambda args, runtime: args)


def test_native_external_callback_runs_from_bytecode_dispatch():
    vm = VirtualMachine()
    vm.register_external("sqlite.open", "native", lambda args, runtime: f"opened:{args[0]}")

    bytecode = bytearray([
        Opcode.PUSH_CONST, 0, 1,
        Opcode.PUSH_CONST, 0, 0,
        Opcode.OP_ASYNC_CALL, 0, 1,
        Opcode.HALT, 0, 0,
    ])
    vm.load(bytecode, ["sqlite.open", "app.db"])
    vm.interpreter.run()

    assert vm.value_stack.pop() == "opened:app.db"