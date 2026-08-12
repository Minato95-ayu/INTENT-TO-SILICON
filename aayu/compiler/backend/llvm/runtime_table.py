from dataclasses import dataclass
from typing import List, Dict, Optional
from aayu.compiler.backend.llvm.values import LLVMModule, LLVMFunction, LLVMArgument
from aayu.compiler.backend.llvm.types import (
    LLVMType, void, i64, i32, i8, ptr, f64, i1
)

@dataclass
class RuntimeSymbol:
    name: str
    return_type: LLVMType
    arg_types: List[LLVMType]
    attributes: List[str]
    linkage: str = "external"
    calling_conv: str = "cdecl"
    library: str = "core"
    min_runtime_version: str = "1.0.0"
    is_required: bool = True
    is_deprecated: bool = False

class RuntimeSymbolTable:
    """
    Manages the stable ABI declarations of the AAYU Native Runtime.
    Provides metadata (attributes, linkage, etc.) for LLVM optimization.
    """
    def __init__(self):
        self.symbols: Dict[str, RuntimeSymbol] = {}
        self._register_all()

    def _register(self, name: str, return_type: LLVMType, arg_types: List[LLVMType], attributes: List[str]):
        self.symbols[name] = RuntimeSymbol(
            name=name,
            return_type=return_type,
            arg_types=arg_types,
            attributes=attributes
        )

    def _register_all(self):
        # Memory
        self._register("aayu_alloc", ptr, [i64], ["nounwind"])
        self._register("aayu_free", void, [ptr], ["nounwind"])
        self._register("aayu_realloc", ptr, [ptr, i64], ["nounwind"])
        self._register("aayu_memcpy", ptr, [ptr, ptr, i64], ["nounwind"])
        self._register("aayu_memmove", ptr, [ptr, ptr, i64], ["nounwind"])
        self._register("aayu_memset", ptr, [ptr, i32, i64], ["nounwind"])

        # IO
        self._register("aayu_print_i64", void, [i64], ["nounwind"])
        self._register("aayu_print_f64", void, [f64], ["nounwind"])
        self._register("aayu_print_bool", void, [i1], ["nounwind"])
        self._register("aayu_print_string", void, [ptr], ["nounwind", "readonly"]) # ptr to AayuString

        # Panic
        # module(ptr), func(ptr), file(ptr), line(i64), col(i64), msg(ptr)
        self._register("aayu_panic", void, [ptr, ptr, ptr, i64, i64, ptr], ["noreturn", "cold"])

        # GC
        self._register("aayu_gc_init", void, [], ["nounwind"])
        self._register("aayu_gc_shutdown", void, [], ["nounwind"])
        self._register("aayu_gc_alloc", ptr, [i64], ["nounwind"])
        self._register("aayu_gc_collect", void, [], ["nounwind"])

    def inject_declarations(self, module: LLVMModule):
        """
        Injects all runtime function declarations into the LLVM Module.
        """
        for sym in self.symbols.values():
            func = LLVMFunction(sym.name, sym.return_type)
            func.is_declare_only = True
            
            # Setup arguments
            for i, arg_type in enumerate(sym.arg_types):
                arg = LLVMArgument(arg_type, f"arg{i}", func)
                func.args.append(arg)
                
            # Add attributes (we will store them in metadata to be emitted by the serializer)
            func.metadata["attributes"] = sym.attributes
            func.metadata["linkage"] = sym.linkage
            
            module.add_function(func)

    def get_symbol(self, name: str) -> Optional[RuntimeSymbol]:
        return self.symbols.get(name)
