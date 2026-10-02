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

"""Explicit Python ecosystem bindings for AAYU interop."""

import importlib


class PythonInteropError(RuntimeError):
    """Raised when a selected Python module function cannot be bound."""


def bind_python_function(vm, module: str, symbol: str, aayu_name: str) -> None:
    if not module or not symbol.isidentifier():
        raise PythonInteropError("Python bindings require a module and simple function name")
    try:
        target = getattr(importlib.import_module(module), symbol)
    except (ImportError, AttributeError) as exc:
        raise PythonInteropError(f"Unable to bind Python function '{module}.{symbol}'") from exc
    if not callable(target):
        raise PythonInteropError(f"Python target '{module}.{symbol}' is not callable")

    def call(args, _vm):
        return target(*args)

    vm.stdlib.register_python_external(aayu_name, call)