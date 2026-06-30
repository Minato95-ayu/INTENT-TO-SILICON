class DebuggerHost:
    """Interface for debugger frontends (CLI, IDE, Tests)."""
    
    def on_pause(self, debugger, vm):
        """Called when execution pauses (breakpoint, step, pause request)."""
        pass
        
    def on_resume(self, debugger, vm):
        """Called when execution resumes."""
        pass
        
    def on_breakpoint(self, debugger, vm, breakpoint):
        """Called specifically when a breakpoint is hit."""
        pass
        
    def on_exception(self, debugger, vm, exception_value):
        """Called when an exception occurs and might cause a pause."""
        pass
        
    def on_output(self, debugger, vm, text: str):
        """Called when the debugger wants to print diagnostic info."""
        pass


class MockDebuggerHost(DebuggerHost):
    """Mock host for automated tests."""
    def __init__(self):
        self.paused = []
        self.events = []
        self.commands = []
        
    def queue_command(self, cmd_fn):
        """Queue a function that will be executed when the VM pauses."""
        self.commands.append(cmd_fn)

    def on_pause(self, debugger, vm):
        self.events.append("PAUSED")
        
        # Save a snapshot of the top frame info
        if vm.frames:
            top_frame = vm.frames[-1]
            # Just capture the function name and IP for the test
            self.paused.append({
                "function": top_frame.frame_name,
                "ip": top_frame.ip
            })
            
        if self.commands:
            cmd = self.commands.pop(0)
            cmd(debugger, vm)
        else:
            # If no commands are queued, default to run so it doesn't hang forever
            debugger.execution_controller.resume()

    def on_resume(self, debugger, vm):
        self.events.append("RESUMED")

    def on_breakpoint(self, debugger, vm, breakpoint):
        self.events.append(f"BREAKPOINT_{breakpoint.id}")
