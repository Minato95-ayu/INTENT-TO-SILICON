from typing import List, Optional, Any
from dataclasses import dataclass, field

@dataclass
class DINode:
    """Base class for all Debug Information Nodes."""
    # Metadata ID for serialization (e.g. !0, !1)
    # This is populated during the serialization phase.
    md_id: Optional[int] = None

@dataclass
class DICompileUnit(DINode):
    language: int
    file: 'DIFile'
    producer: str
    is_optimized: bool
    runtime_version: int
    emission_kind: int
    
    def serialize_content(self) -> str:
        return (f"!DICompileUnit(language: {self.language}, "
                f"file: !{self.file.md_id}, "
                f"producer: \"{self.producer}\", "
                f"isOptimized: {'true' if self.is_optimized else 'false'}, "
                f"runtimeVersion: {self.runtime_version}, "
                f"emissionKind: {self.emission_kind})")

@dataclass
class DIFile(DINode):
    filename: str
    directory: str
    
    def serialize_content(self) -> str:
        return f"!DIFile(filename: \"{self.filename}\", directory: \"{self.directory}\")"

@dataclass
class DISubprogram(DINode):
    name: str
    linkage_name: str
    scope: DINode
    file: DIFile
    line: int
    is_local: bool
    is_definition: bool
    scope_line: int
    unit: DICompileUnit
    
    def serialize_content(self) -> str:
        return (f"!DISubprogram(name: \"{self.name}\", "
                f"linkageName: \"{self.linkage_name}\", "
                f"scope: !{self.scope.md_id}, "
                f"file: !{self.file.md_id}, "
                f"line: {self.line}, "
                f"isLocal: {'true' if self.is_local else 'false'}, "
                f"isDefinition: {'true' if self.is_definition else 'false'}, "
                f"scopeLine: {self.scope_line}, "
                f"unit: !{self.unit.md_id})")

@dataclass
class DILexicalBlock(DINode):
    scope: DINode
    file: DIFile
    line: int
    column: int
    
    def serialize_content(self) -> str:
        return (f"!DILexicalBlock(scope: !{self.scope.md_id}, "
                f"file: !{self.file.md_id}, "
                f"line: {self.line}, "
                f"column: {self.column})")

@dataclass
class DILocation(DINode):
    line: int
    column: int
    scope: DINode
    
    def serialize_content(self) -> str:
        return (f"!DILocation(line: {self.line}, "
                f"column: {self.column}, "
                f"scope: !{self.scope.md_id})")
