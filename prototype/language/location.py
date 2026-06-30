from dataclasses import dataclass

@dataclass
class SourceFile:
    id: int
    path: str
    module: str

@dataclass
class SourceSpan:
    file_id: int
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    
    def __str__(self):
        return f"file_id={self.file_id}:{self.start_line}:{self.start_column}-{self.end_line}:{self.end_column}"
