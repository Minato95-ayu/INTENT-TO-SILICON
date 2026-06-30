from typing import List, Optional, Any

class AAYUType:
    """Base class for all semantic types in AAYU."""
    def __init__(self, name: str):
        self.name = name

    def is_assignable_from(self, other: 'AAYUType') -> bool:
        """
        Check if an object of type `other` can be assigned to a variable of this type.
        MVP Phase 5.3: Strict equality unless AnyType, UnknownType, or ErrorType is involved.
        """
        if isinstance(other, AnyType) or isinstance(other, UnknownType) or isinstance(other, ErrorType):
            return True
        if isinstance(self, AnyType) or isinstance(self, UnknownType) or isinstance(self, ErrorType):
            return True
        
        # Primitive types match by name
        if isinstance(self, PrimitiveType) and isinstance(other, PrimitiveType):
            return self.name == other.name
            
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

class PrimitiveType(AAYUType):
    """Represents builtin primitives like Number, Text, Boolean."""
    pass

class AnyType(AAYUType):
    """Represents a dynamically typed or untyped value."""
    def __init__(self):
        super().__init__("Any")

class VoidType(AAYUType):
    """Represents the absence of a value (e.g., function with no return)."""
    def __init__(self):
        super().__init__("Void")

class UnknownType(AAYUType):
    """Represents a type that could not be resolved. Used for future inference."""
    def __init__(self):
        super().__init__("Unknown")

class ErrorType(AAYUType):
    """Represents a type error. Prevents cascading compiler errors."""
    def __init__(self):
        super().__init__("Error")

class FunctionType(AAYUType):
    """Represents a callable function with parameter types and a return type."""
    def __init__(self, param_types: List[AAYUType], return_type: AAYUType):
        super().__init__("Function")
        self.param_types = param_types
        self.return_type = return_type

    def is_assignable_from(self, other: 'AAYUType') -> bool:
        if isinstance(other, AnyType) or isinstance(other, UnknownType) or isinstance(other, ErrorType):
            return True
        if not isinstance(other, FunctionType):
            return False
            
        if len(self.param_types) != len(other.param_types):
            return False
            
        for t1, t2 in zip(self.param_types, other.param_types):
            if not t1.is_assignable_from(t2):
                return False
                
        return self.return_type.is_assignable_from(other.return_type)

    def __str__(self):
        params = ", ".join(str(p) for p in self.param_types)
        return f"({params}) -> {self.return_type}"


class InterfaceType(AAYUType):
    """Represents an interface definition with required methods."""
    def __init__(self, name: str, methods: dict):
        super().__init__(name)
        self.methods = methods # Dict[str, FunctionType]

    def is_assignable_from(self, other: 'AAYUType') -> bool:
        if isinstance(other, AnyType) or isinstance(other, UnknownType) or isinstance(other, ErrorType):
            return True
        if not isinstance(other, InterfaceType):
            return False
            
        # Nominal subtyping for MVP: must be the exact same interface
        # Future (Phase 5.6+): Structural subtyping or explicit 'implements'
        return self.name == other.name

    def __str__(self):
        return f"Interface {self.name}"

class BuiltinTypes:
    """Registry of builtin singleton types."""
    Number = PrimitiveType("Number")
    Text = PrimitiveType("Text")
    Boolean = PrimitiveType("Boolean")
    Any = AnyType()
    Void = VoidType()
    Unknown = UnknownType()
    Error = ErrorType()

    _registry = {
        "Number": Number,
        "Text": Text,
        "Boolean": Boolean,
        "Any": Any,
        "Void": Void
    }

    @classmethod
    def get(cls, name: str) -> Optional[AAYUType]:
        return cls._registry.get(name)
