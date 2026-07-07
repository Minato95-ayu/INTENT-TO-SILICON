class ContextMemory:
    def __init__(self):
        self.history = []
        self.active_constraints = set()
        
    def add_interaction(self, prompt, ir):
        self.history.append({"prompt": prompt, "ir": ir})
        for c in ir.constraints:
            self.active_constraints.add(c)
            
    def get_contextual_constraints(self):
        return list(self.active_constraints)
