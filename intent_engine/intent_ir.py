class IntentIR:
    def __init__(self):
        self.goal = ""
        self.domains = []
        self.entities = []
        self.constraints = []
        self.non_functional = {
            "security": "",
            "performance": "",
            "availability": "",
            "budget": "",
            "latency": ""
        }
        self.deployment = {}
        self.architecture = {}
        self.workflows = []
        self.clarifications = []
        self.confidence = 0.0

    def to_dict(self):
        return {
            "goal": self.goal,
            "domains": self.domains,
            "entities": self.entities,
            "constraints": self.constraints,
            "non_functional": self.non_functional,
            "deployment": self.deployment,
            "architecture": self.architecture,
            "workflows": self.workflows,
            "clarifications": self.clarifications,
            "confidence": self.confidence
        }
