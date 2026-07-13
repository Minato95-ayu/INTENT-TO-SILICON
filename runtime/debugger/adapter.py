import socket
import threading
from .session import DebugSession

class DAPAdapter:
    """TCP Server for remote debugging."""
    
    def __init__(self, debugger, host='127.0.0.1', port=4711):
        self.debugger = debugger
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.running = True
        
        # Run in background thread
        thread = threading.Thread(target=self._accept_loop, daemon=True)
        thread.start()
        
    def _accept_loop(self):
        while self.running:
            try:
                client_sock, _ = self.server_socket.accept()
                session = DebugSession(client_sock, self.debugger)
                session.start()
            except Exception:
                if self.running:
                    pass # Log error
                    
    def stop(self):
        self.running = False
        self.server_socket.close()
