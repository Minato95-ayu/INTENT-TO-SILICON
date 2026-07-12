class IntentHistory:
    def __init__(self):
        self.history = []
    def add(self, intent):
        self.history.append(intent)
    def get_last(self):
        return self.history[-1] if self.history else None
