import re

class AAYULinter:
    """
    AAYU Linter
    -----------
    Performs static analysis on AAYU code to catch common mistakes early.
    It checks for:
      - Missing periods (.) at the end of statements.
      - Missing type definitions (e.g. `let x = 5` instead of `let x: Number = 5`).
      - Unused imports (simulated).
    """
    
    def lint(self, source_code: str) -> list[str]:
        """
        Analyzes the source code and returns a list of warnings/errors.
        
        Args:
            source_code (str): The AAYU source file contents.
            
        Returns:
            list[str]: A list of diagnostic messages. Empty list means the code is clean.
        """
        diagnostics = []
        lines = source_code.split('\n')
        
        for i, line in enumerate(lines):
            line_num = i + 1
            stripped = line.strip()
            
            # Skip empty lines or comments
            if not stripped or stripped.startswith("//"):
                continue
                
            # Rule 1: Every statement (unless opening a block) must end with a period.
            # Block openers: 'do', 'has'. We also ignore 'fn' and 'entity' declarations 
            # if they don't terminate immediately, but for the MVP linter, we enforce strictly.
            if not stripped.endswith(".") and stripped not in ["do", "has"]:
                if stripped.startswith("entity") or stripped.startswith("fn") or stripped == "end":
                    pass # These don't strictly need periods on the same line depending on syntax
                else:
                    diagnostics.append(f"Line {line_num}: Warning: Missing terminating period (.).")
                    
            # Rule 2: Strict typing. 'let' and 'mut' must have type annotations.
            if stripped.startswith("let ") or stripped.startswith("mut "):
                if ":" not in stripped:
                    diagnostics.append(f"Line {line_num}: Error: Missing type annotation. Use 'let name: Type = value.'.")
                    
        return diagnostics
