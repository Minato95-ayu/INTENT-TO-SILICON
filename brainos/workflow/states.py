from enum import Enum

class WorkflowState(str, Enum):
    PLANNING = "PLANNING"
    GUARD = "GUARD"
    READY = "READY"
    EXECUTING = "EXECUTING"
    CRITIQUE = "CRITIQUE"
    IMPACT = "IMPACT"
    SNAPSHOT = "SNAPSHOT"
    DONE = "DONE"
    FAILED = "FAILED"
