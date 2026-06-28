from typing import List, Dict, Any, Optional

class Question:
    def __init__(self, data: Dict[str, Any]):
        self.id = data["id"]
        self.text = data["text"]
        self.type = data["type"]
        self.options = data.get("options", [])
        self.next_q = data.get("next")  # ID of next question, if static
    
    def format_prompt(self) -> str:
        prompt = f"\n{self.text}\n"
        if self.type == "choice":
            for i, opt in enumerate(self.options, 1):
                prompt += f"{i}. {opt}\n"
            prompt += "> "
        elif self.type == "boolean":
            prompt += "(Y/N)\n> "
        else:
            prompt += "> "
        return prompt

    def validate_answer(self, answer: str) -> bool:
        if self.type == "choice":
            if answer.isdigit():
                idx = int(answer) - 1
                return 0 <= idx < len(self.options)
            return answer in self.options
        elif self.type == "boolean":
            return answer.upper() in ["Y", "N", "YES", "NO"]
        return True

    def parse_answer(self, answer: str) -> Any:
        if self.type == "choice":
            if answer.isdigit():
                idx = int(answer) - 1
                return self.options[idx]
            return answer
        elif self.type == "boolean":
            return answer.upper() in ["Y", "YES"]
        return answer
