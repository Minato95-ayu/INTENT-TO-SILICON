import re
import json

class AIHallucinationError(Exception):
    def __init__(self, message, hint):
        self.message = message
        self.hint = hint
        # The AI agent can parse this JSON to self-correct
        self.json_feedback = json.dumps({
            "error_type": "AI_HALLUCINATION",
            "message": message,
            "actionable_hint": hint
        }, indent=2)
        super().__init__(self.json_feedback)

class AIGuardian:
    """
    The AI-Guardian acts as an Auto-Receiver that blocks LLM hallucinations 
    before they even hit the parser, providing machine-readable corrections.
    """
    
    FORBIDDEN_PATTERNS = [
        (re.compile(r'^\s*import\s+.*', re.MULTILINE), 
         "AAYU has zero dependencies. Do not use 'import'. Use native AAYU features (e.g., File I/O, Web API)."),
         
        (re.compile(r'^\s*from\s+.*\s+import\s+.*', re.MULTILINE), 
         "AAYU does not support 'from X import Y'. Everything is built-in natively."),
         
        (re.compile(r'^\s*require\s*\(.*', re.MULTILINE), 
         "AAYU is not JavaScript. Do not use 'require()'. Use native built-ins."),
         
        (re.compile(r'^\s*pip\s+install.*', re.MULTILINE), 
         "AAYU is not Python. There is no 'pip'. Remove installation commands."),
         
        (re.compile(r'^\s*npm\s+install.*', re.MULTILINE), 
         "AAYU is not Node.js. There is no 'npm'. Remove installation commands.")
    ]

    @classmethod
    def scan_source(cls, source_code: str):
        """Scans the raw source code for known AI hallucinations."""
        for pattern, hint in cls.FORBIDDEN_PATTERNS:
            match = pattern.search(source_code)
            if match:
                raise AIHallucinationError(
                    message=f"Forbidden syntax detected: '{match.group(0).strip()}'",
                    hint=hint
                )
        return True

    @classmethod
    def parse_intent(cls, intent_text: str):
        """
        Parses intent blocks for AI alignment.
        """
        cleaned = intent_text.strip()
        return {"type": "IntentBlock", "description": cleaned}
