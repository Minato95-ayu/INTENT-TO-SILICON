class EventDispatcher:
    def __init__(self, vm):
        self.vm = vm
        self.on_state_changed = None
        
    def dispatch(self, action_name: str):
        print(f"[EventDispatcher] Dispatching action: {action_name}")
        self.vm.call_action_by_name(action_name)
        
        # After action completes, the state is updated.
        # Trigger a re-render!
        if self.on_state_changed:
            self.on_state_changed()
