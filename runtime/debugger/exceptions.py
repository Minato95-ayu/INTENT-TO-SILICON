class DebuggerError(Exception):
    pass

class EvaluationError(DebuggerError):
    pass

class DisconnectedError(DebuggerError):
    pass
