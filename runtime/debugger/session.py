from .protocol import DAPProtocol
from .snapshot import VMSnapshot
from .callstack import CallStackFormatter
from .variables import VariableInspector

class DebugSession:
    """Manages a single client connection."""
    
    def __init__(self, socket, debugger):
        self.socket = socket
        self.debugger = debugger
        self.protocol = DAPProtocol(socket.makefile('r'), socket.makefile('w'))
        
    def start(self):
        while True:
            msg = self.protocol.read_message()
            if not msg:
                break
                
            if msg["type"] == "request":
                self.handle_request(msg)
                
    def handle_request(self, req):
        cmd = req["command"]
        if cmd == "initialize":
            self.protocol.send_response(req, {
                "supportsConfigurationDoneRequest": True,
                "supportsEvaluateForHovers": True,
                "supportsStepBack": False, # Technical debt
                "supportsSetVariable": False
            })
        elif cmd == "launch":
            self.protocol.send_response(req)
            self.protocol.send_event("initialized")
        elif cmd == "setBreakpoints":
            lines = req["params"].get("breakpoints", [])
            for bp in lines:
                self.debugger.breakpoints.set_breakpoint(bp["line"])
            self.protocol.send_response(req, {"breakpoints": lines})
        elif cmd == "configurationDone":
            self.protocol.send_response(req)
        elif cmd == "continue":
            self.protocol.send_response(req)
            self.debugger.resume()
        elif cmd == "next": # Step Over
            self.protocol.send_response(req)
            self.debugger.step_over()
        elif cmd == "stepIn":
            self.protocol.send_response(req)
            self.debugger.step_into()
        elif cmd == "stepOut":
            self.protocol.send_response(req)
            self.debugger.step_out()
        elif cmd == "pause":
            self.protocol.send_response(req)
            self.debugger.pause()
        elif cmd == "stackTrace":
            if self.debugger.snapshot:
                fmt = CallStackFormatter(self.debugger.snapshot, self.debugger.debug_map)
                self.protocol.send_response(req, {"stackFrames": fmt.get_frames(), "totalFrames": len(fmt.get_frames())})
            else:
                self.protocol.send_response(req, {"stackFrames": [], "totalFrames": 0})
        elif cmd == "disconnect":
            self.protocol.send_response(req)
            self.debugger.resume()
        else:
            self.protocol.send_response(req)
