"""Explicit C-ABI loading for AAYU native interop."""

import ctypes
import ctypes.util
from typing import Callable, Optional, Sequence


_TYPE_MAP = {
    "Int": ctypes.c_int64,
    "Float": ctypes.c_double,
    "Bool": ctypes.c_bool,
    "String": ctypes.c_char_p,
    "Null": None,
}


class NativeInteropError(RuntimeError):
    """Raised when a native library or symbol cannot be safely bound."""


def _resolve_type(type_name: str):
    try:
        return _TYPE_MAP[type_name]
    except KeyError as exc:
        raise NativeInteropError(f"Unsupported native ABI type: {type_name}") from exc


class NativeLibrary:
    """Loads explicitly selected C-ABI functions and adapts them to AAYU calls."""

    def __init__(self, library: str):
        path = ctypes.util.find_library(library) or library
        try:
            self.handle = ctypes.CDLL(path)
        except OSError as exc:
            raise NativeInteropError(f"Unable to load native library '{library}'") from exc

    def bind(
        self,
        symbol: str,
        return_type: str,
        argument_types: Sequence[str],
    ) -> Callable:
        if not symbol or not symbol.isidentifier():
            raise NativeInteropError(f"Invalid native symbol: {symbol!r}")

        function = getattr(self.handle, symbol, None)
        if function is None:
            raise NativeInteropError(f"Native symbol '{symbol}' was not found")

        c_return_type = _resolve_type(return_type)
        c_argument_types = [_resolve_type(type_name) for type_name in argument_types]
        function.restype = c_return_type
        function.argtypes = c_argument_types

        def call(args, _vm):
            if len(args) != len(c_argument_types):
                raise NativeInteropError(
                    f"Native function '{symbol}' expects {len(c_argument_types)} arguments, got {len(args)}"
                )
            converted = []
            for value, type_name in zip(args, argument_types):
                converted.append(value.encode("utf-8") if type_name == "String" else value)
            result = function(*converted)
            if return_type == "String" and result is not None:
                return result.decode("utf-8")
            return result

        return call


def bind_native_function(
    vm,
    library: str,
    symbol: str,
    aayu_name: str,
    return_type: str,
    argument_types: Sequence[str],
) -> None:
    """Load one C-ABI function and register it as a native AAYU callback."""
    native_library = NativeLibrary(library)
    callback = native_library.bind(symbol, return_type, argument_types)
    vm.register_external(aayu_name, "native", callback)
    if not hasattr(vm, "native_libraries"):
        vm.native_libraries = []
    vm.native_libraries.append(native_library)
