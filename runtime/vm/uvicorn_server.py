import sys
import uvicorn
import asyncio
import threading

class UvicornServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass # Disable signal handlers since we run in a thread

    def run_in_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop_server(self):
        self.should_exit = True
        if hasattr(self, 'thread'):
            self.thread.join(timeout=5)
