from lsprotocol.types import Diagnostic, DiagnosticSeverity, Range, Position

class DiagnosticTranslator:
    @staticmethod
    def translate_error(error) -> Diagnostic:
        line = max(0, error.line - 1)
        col = max(0, error.column - 1)
        return Diagnostic(
            range=Range(
                start=Position(line=line, character=col),
                end=Position(line=line, character=col + 5)
            ),
            message=str(error),
            severity=DiagnosticSeverity.Error,
            source="aayu-compiler"
        )
