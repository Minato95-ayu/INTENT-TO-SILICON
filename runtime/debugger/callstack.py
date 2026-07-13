class CallStackFormatter:
    """Translates VM CallStack into DAP-compliant stack traces."""
    
    def __init__(self, snapshot, debug_map=None):
        self.snapshot = snapshot
        self.debug_map = debug_map or {}
        
    def get_frames(self):
        frames = []
        for i, frame in enumerate(reversed(self.snapshot.call_stack)):
            ip = frame["ip"]
            # Map IP to Line using debug_map
            line_info = self.debug_map.get(ip, {"line": 0, "file": "unknown"})
            
            frames.append({
                "id": i,
                "name": frame["function"] or "main",
                "line": line_info["line"],
                "column": 0,
                "source": {"name": line_info["file"], "path": line_info["file"]}
            })
        return frames
