with open('runtime/ui/events.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_event = '''class EventDispatcher:
    def __init__(self, vm):
        self.vm = vm
        
    def dispatch(self, action_name: str):
        # We need to tell the VM to execute an action by name
        print(f"[EventDispatcher] Dispatching action: {action_name}")
        self.vm.call_action_by_name(action_name)'''

new_event = '''class EventDispatcher:
    def __init__(self, vm):
        self.vm = vm
        self.on_state_changed = None
        
    def dispatch(self, action_name: str):
        print(f"[EventDispatcher] Dispatching action: {action_name}")
        self.vm.call_action_by_name(action_name)
        
        # After action completes, the state is updated.
        # Trigger a re-render!
        if self.on_state_changed:
            self.on_state_changed()'''

content = content.replace(old_event, new_event)

with open('runtime/ui/events.py', 'w', encoding='utf-8') as f:
    f.write(content)
