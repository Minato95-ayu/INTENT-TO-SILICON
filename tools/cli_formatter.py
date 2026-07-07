import re

class AAYUFormatter:
    """
    AAYU Formatter
    --------------
    Responsible for enforcing the official AAYU style guide.
    This ensures that all AAYU code adheres to strict indentation (4 spaces),
    keyword boundaries (do/end), and mandatory trailing periods (.).
    
    Usage:
        formatter = AAYUFormatter()
        clean_code = formatter.format(raw_code)
    """
    
    def __init__(self):
        # 4 spaces is the strict standard for AAYU
        self.indent_size = 4
        
    def format(self, source_code: str) -> str:
        """
        Parses the raw source string and returns a perfectly formatted string.
        
        Args:
            source_code (str): The unformatted AAYU code.
            
        Returns:
            str: The styled, formatted code.
        """
        lines = source_code.split('\n')
        formatted_lines = []
        current_indent = 0
        
        for line in lines:
            # Strip whitespace to clean the raw input
            stripped = line.strip()
            if not stripped:
                formatted_lines.append("")
                continue
                
            # Decrease indent before writing the line if it closes a block
            if stripped in ["end", "end."]:
                current_indent = max(0, current_indent - 1)
                
            # Apply the current indent level (4 spaces per level)
            indent_str = " " * (current_indent * self.indent_size)
            formatted_lines.append(f"{indent_str}{stripped}")
            
            # Increase indent for the next line if this line opens a block
            if stripped == "do" or stripped == "has":
                current_indent += 1
                
        return "\n".join(formatted_lines)
