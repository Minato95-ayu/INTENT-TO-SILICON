class SteppingController:
    """Computes target IPs for Step Into, Step Over, Step Out."""
    
    def __init__(self, debug_map):
        self.debug_map = debug_map
        self.target_line = None
        self.mode = None
        
    def step_into(self):
        self.mode = "into"
        
    def step_over(self, current_line: int):
        self.mode = "over"
        self.target_line = current_line + 1
        
    def step_out(self):
        self.mode = "out"
        
    def should_break(self, current_ip: int, current_frame_depth: int, target_frame_depth: int) -> bool:
        if self.mode == "into":
            # Break on any new instruction that maps to a line
            return current_ip in self.debug_map
            
        elif self.mode == "over":
            if current_ip in self.debug_map:
                line = self.debug_map[current_ip]["line"]
                if line >= self.target_line and current_frame_depth <= target_frame_depth:
                    self.mode = None
                    return True
            return False
            
        elif self.mode == "out":
            if current_frame_depth < target_frame_depth:
                self.mode = None
                return True
            return False
            
        return False
