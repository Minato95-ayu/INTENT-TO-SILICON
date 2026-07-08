from runtime.base import BaseRuntime
from runtime.ui.adapters.native_ui_adapter import NativeUIAdapter

class UIRuntime(BaseRuntime):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.adapter = None

    def initialize(self):
        ui_ir = self.metadata.get("ui_ir", {})
        
        # We can dynamically configure the port if specified in config, else default to 8080
        self.adapter = NativeUIAdapter(port=8080, ui_ir=ui_ir)
        self.adapter.initialize()

    def start(self):
        self.adapter.start()
