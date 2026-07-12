"""
=============================================================================
FILE: executor.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from abc import ABC, abstractmethod
from ..task.task import Task

class ExecutorProvider(ABC):
    @abstractmethod
    def execute(self, task: Task) -> str:
        """Execute the task and return result ('PASS', 'FAIL', 'SKIP')."""
        pass

class HumanApprovalExecutor(ExecutorProvider):
    def execute(self, task: Task) -> str:
        print("\n" + "="*50)
        print(f"TASK EXECUTION REQUIRED: {task.id}")
        print(f"Description: {task.description}")
        print("="*50)
        
        while True:
            result = input("Mark task result (PASS / FAIL / SKIP): ").strip().upper()
            if result in ("PASS", "FAIL", "SKIP"):
                return result
            print("Invalid input. Please enter PASS, FAIL, or SKIP.")
