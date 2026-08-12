from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any, ClassVar

class Type:
    """Base class for all AAYU Types."""
    
    def is_assignable_to(self, other: 'Type') -> bool:
        """Check if this type can be assigned to another type."""
        # Any type is assignable to Any
        if isinstance(other, PrimitiveType) and other.name == "Any":
            return True
        # Union assignment: T is assignable to A | B if T is assignable to A or B
        if isinstance(other, UnionType):
            return any(self.is_assignable_to(u) for u in other.types)
        # Exact match fallback
        return self == other
        
    def __eq__(self, other):
        return isinstance(other, type(self))

@dataclass
class PrimitiveType(Type):
    name: str  # Int, Float, String, Bool, Char, Byte, Void, Never, Any, Null
    
    def __eq__(self, other):
        return isinstance(other, PrimitiveType) and self.name == other.name
        
    def __hash__(self):
        return hash(self.name)
        
    def __str__(self):
        return self.name

@dataclass
class UnionType(Type):
    types: frozenset[Type]
    
    def __init__(self, *types: Type):
        # Flatten nested unions and remove duplicates
        flat_types = set()
        for t in types:
            if isinstance(t, UnionType):
                flat_types.update(t.types)
            else:
                flat_types.add(t)
        self.types = frozenset(flat_types)
        
    def __eq__(self, other):
        return isinstance(other, UnionType) and self.types == other.types
        
    def __hash__(self):
        return hash(self.types)
        
    def __str__(self):
        return " | ".join(sorted(str(t) for t in self.types))
        
    def is_assignable_to(self, other: 'Type') -> bool:
        if isinstance(other, PrimitiveType) and other.name == "Any":
            return True
        # A | B is assignable to C iff both A is assignable to C AND B is assignable to C
        return all(t.is_assignable_to(other) for t in self.types)

@dataclass
class OptionalType(Type):
    inner: Type
    
    def __str__(self):
        return f"Optional<{self.inner}>"
        
    def is_assignable_to(self, other: 'Type') -> bool:
        if isinstance(other, PrimitiveType) and other.name == "Any":
            return True
        if isinstance(other, OptionalType):
            return self.inner.is_assignable_to(other.inner)
        if isinstance(other, UnionType):
            return any(self.is_assignable_to(u) for u in other.types)
        return False
        
    def __eq__(self, other):
        return isinstance(other, OptionalType) and self.inner == other.inner
        
    def __hash__(self):
        return hash(("Optional", self.inner))

# Built-in primitive singletons for performance and memory safety (Gate 10)
T_INT = PrimitiveType("Int")
T_FLOAT = PrimitiveType("Float")
T_STRING = PrimitiveType("String")
T_BOOL = PrimitiveType("Bool")
T_CHAR = PrimitiveType("Char")
T_BYTE = PrimitiveType("Byte")
T_VOID = PrimitiveType("Void")
T_NEVER = PrimitiveType("Never")
T_ANY = PrimitiveType("Any")
T_NULL = PrimitiveType("Null")

# Helper for Nullable (T?) -> Union<T, Null>
def make_nullable(inner: Type) -> UnionType:
    return UnionType(inner, T_NULL)

# Future Stubs for subsequent phases
class PointerType(Type): pass
class ReferenceType(Type): pass
class ArrayType(Type): pass
class SliceType(Type): pass
class TupleType(Type): pass
import hashlib

class FieldID(int): pass
class VariantID(int): pass

@dataclass
class StructField:
    name: str
    field_type: Type
    index: int  # legacy index
    field_id: FieldID = field(default_factory=lambda: FieldID(0))
    
    _field_id_registry: ClassVar[Dict[FieldID, str]] = {}

    def generate_id(self, struct_qualified_name: str):
        # ModuleID + TypeID + Canonical Name
        canonical = f"{struct_qualified_name}.{self.name}"
        hash_bytes = hashlib.sha256(canonical.encode('utf-8')).digest()
        fid = FieldID(int.from_bytes(hash_bytes[:8], byteorder='big'))
        
        if fid in StructField._field_id_registry and StructField._field_id_registry[fid] != canonical:
            from aayu.compiler.semantic.context import IDCollisionError
            raise IDCollisionError(fid, StructField._field_id_registry[fid], canonical, "SemanticContext / FieldID")
            
        StructField._field_id_registry[fid] = canonical
        self.field_id = fid

@dataclass
class StructType(Type):
    """
    Production-grade Struct type representation.
    """
    name: str
    fields: List[StructField] = field(default_factory=list)
    # Metadata for compiler pipeline
    size: int = 0
    alignment: int = 0
    field_count: int = 0
    field_offsets: List[int] = field(default_factory=list)
    visibility: str = "public"
    methods: List[str] = field(default_factory=list)
    traits: List[str] = field(default_factory=list)
    generic_params: List[str] = field(default_factory=list)
    attributes: List[str] = field(default_factory=list)

    def get_field(self, name: str) -> Optional[StructField]:
        for f in self.fields:
            if f.name == name:
                return f
        return None
        
    def calculate_layout(self):
        """Calculates size, alignment, and field offsets based on the target ABI."""
        self.size = 0
        self.alignment = 1
        self.field_offsets = []
        
        for f in self.fields:
            # Very basic ABI simulation (e.g. 32-bit/64-bit generic)
            # We assume Int is 4 bytes, String is 8 bytes (ptr), etc.
            f_size = 8
            f_align = 8
            
            if isinstance(f.field_type, PrimitiveType):
                if f.field_type.name in ["Int", "Float"]:
                    f_size = 4
                    f_align = 4
                elif f.field_type.name == "Bool":
                    f_size = 1
                    f_align = 1
            elif isinstance(f.field_type, StructType):
                f_size = f.field_type.size
                f_align = f.field_type.alignment
                
            # align current size
            if self.size % f_align != 0:
                self.size += f_align - (self.size % f_align)
                
            self.field_offsets.append(self.size)
            self.size += f_size
            self.alignment = max(self.alignment, f_align)
            
        # tail padding
        if self.alignment > 0 and self.size % self.alignment != 0:
            self.size += self.alignment - (self.size % self.alignment)
            
        self.field_count = len(self.fields)

    def is_assignable_to(self, other: 'Type') -> bool:
        if isinstance(other, PrimitiveType) and other.name == "Any":
            return True
        if isinstance(other, UnionType):
            return any(self.is_assignable_to(u) for u in other.types)
        return isinstance(other, StructType) and self.name == other.name

    def __eq__(self, other):
        return isinstance(other, StructType) and self.name == other.name

    def __hash__(self):
        return hash(("Struct", self.name))

    def __str__(self):
        return self.name
@dataclass
class EnumVariant:
    """Represents a single variant of an enum. Designed for future payload support."""
    name: str
    tag: int  # legacy tag/index
    variant_id: VariantID = field(default_factory=lambda: VariantID(0))
    # Future: payload_types will hold List[Type] for ADT variants like Ok(String)
    payload_types: List['Type'] = field(default_factory=list)
    
    _variant_id_registry: ClassVar[Dict[VariantID, str]] = {}
    
    def generate_id(self, enum_qualified_name: str):
        canonical = f"{enum_qualified_name}.{self.name}"
        hash_bytes = hashlib.sha256(canonical.encode('utf-8')).digest()
        vid = VariantID(int.from_bytes(hash_bytes[:8], byteorder='big'))
        
        if vid in EnumVariant._variant_id_registry and EnumVariant._variant_id_registry[vid] != canonical:
            from aayu.compiler.semantic.context import IDCollisionError
            raise IDCollisionError(vid, EnumVariant._variant_id_registry[vid], canonical, "SemanticContext / VariantID")
            
        EnumVariant._variant_id_registry[vid] = canonical
        self.variant_id = vid

    def __eq__(self, other):
        return isinstance(other, EnumVariant) and self.name == other.name and self.tag == other.tag

    def __hash__(self):
        return hash((self.name, self.tag))

    def __str__(self):
        if self.payload_types:
            payload_str = ", ".join(str(t) for t in self.payload_types)
            return f"{self.name}({payload_str})"
        return self.name

@dataclass
class EnumType(Type):
    """
    Production-grade Enum type representation.
    
    Design philosophy: The compiler IR preserves EnumType identity throughout
    the entire pipeline. Only the final backend lowering converts to i32/i16/i8
    based on target architecture. This ensures:
      - Color != Int at the compiler level (always)
      - Future payload/ADT enums require zero compiler rewrite
      - Debugger metadata can resolve tag -> variant name
      - Pattern matching can verify exhaustiveness
    """
    name: str
    variants: List[EnumVariant] = field(default_factory=list)
    # Layout metadata for backend lowering
    tag_size: int = 32  # bits: 8, 16, 32 - backend decides final representation
    payload_layout: Optional[List[int]] = None  # Future: byte offsets for payload fields

    def variant_by_name(self, variant_name: str) -> Optional[EnumVariant]:
        """Lookup a variant by name. Returns None if not found."""
        for v in self.variants:
            if v.name == variant_name:
                return v
        return None

    def variant_count(self) -> int:
        return len(self.variants)

    def is_assignable_to(self, other: 'Type') -> bool:
        """
        EnumType assignment rules:
        - Color is assignable to Color (exact match)
        - Color is assignable to Any
        - Color is NEVER assignable to Int (strict separation)
        - Color is assignable to Union if any member matches
        """
        if isinstance(other, PrimitiveType) and other.name == "Any":
            return True
        if isinstance(other, UnionType):
            return any(self.is_assignable_to(u) for u in other.types)
        # Strict: only same-name enum is assignable
        return isinstance(other, EnumType) and self.name == other.name

    def __eq__(self, other):
        return isinstance(other, EnumType) and self.name == other.name

    def __hash__(self):
        return hash(("Enum", self.name))

    def __str__(self):
        return self.name
class TraitType(Type): pass
class InterfaceType(Type): pass
class FunctionType(Type): pass
class GenericParameterType(Type): pass
class GenericInstanceType(Type): pass
