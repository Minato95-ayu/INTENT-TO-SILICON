import threading
import uuid
import time
from typing import Dict, Any

from runtime.vm.vm import VirtualMachine
from runtime.vm.config import VMConfig
from runtime.events.queue import EventQueue

class Session:
    def __init__(self, session_id: str, prog: Any):
        self.session_id = session_id
        self.event_queue = EventQueue()
        self.vm = VirtualMachine(VMConfig())
        self.vm.interpreter.event_queue = self.event_queue
        # The renderer per session will be stubbed, as the main WebRenderer will handle it.
        # Actually, each VM expects a .renderer to exist, which has a .shutdown() or nothing.
        class DummyRenderer:
            pass
        self.vm.renderer = DummyRenderer()
        self.vm.load(prog.bytecode, prog.constant_pool, prog.action_addresses)
        self.vm.execute()
        self.vm.call_action_by_name("__PAGE_START__")
        self.last_accessed = time.time()
        
        # We need to maintain a current JSON string of the rendered tree for this session
        self.current_tree_json = "{}"
        
        # We need an SSE queue for the client stream
        import queue
        self.message_queue = queue.Queue()
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
    def _run_loop(self):
        import time
        from runtime.renderers.web_renderer import serialize_node
        import json
        while self.running:
            if self.event_queue.has_events():
                evt = self.event_queue.pop()
                if evt.__class__.__name__ == "ActionEvent":
                    self.vm.call_action_by_name(evt.action_name)
                elif evt.__class__.__name__ == "InputEvent":
                    self.vm.update_state(evt.target_state, evt.value)
                    
                if self.vm.router.current_route:
                    self.vm.call_action_by_name(f"__PAGE_START_{self.vm.router.current_route.name}")
                else:
                    self.vm.call_action_by_name("__PAGE_START__")
            
            # Serialize the tree
            if self.vm.interpreter.render_tree:
                style_sheet = set()
                tree_dict = serialize_node(self.vm.interpreter.render_tree.root, style_sheet)
                data = {
                    "tree": tree_dict,
                    "styles": list(style_sheet),
                    "route": {"path": self.vm.router.current_route.path} if self.vm.router.current_route else {}
                }
                new_json = json.dumps(data)
                if new_json != self.current_tree_json:
                    self.current_tree_json = new_json
                    try:
                        self.message_queue.put_nowait(new_json)
                    except queue.Full:
                        pass
                        
            time.sleep(0.016)
            
    def touch(self):
        self.last_accessed = time.time()
        
    def shutdown(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

class SessionManager:
    def __init__(self, prog: Any, session_timeout: int = 3600):
        self.prog = prog
        self.session_timeout = session_timeout
        self.sessions: Dict[str, Session] = {}
        self.lock = threading.RLock()
        
    def get_or_create_session(self, session_id: str) -> Session:
        with self.lock:
            if not session_id or session_id not in self.sessions:
                session_id = str(uuid.uuid4())
                self.sessions[session_id] = Session(session_id, self.prog)
                print(f"[SessionManager] Created new session: {session_id}")
            
            session = self.sessions[session_id]
            session.touch()
            return session
            
    def get_session(self, session_id: str) -> Session:
        with self.lock:
            if session_id in self.sessions:
                session = self.sessions[session_id]
                session.touch()
                return session
            return None
            
    def cleanup_stale_sessions(self):
        with self.lock:
            now = time.time()
            stale_ids = []
            for sid, sess in self.sessions.items():
                if now - sess.last_accessed > self.session_timeout:
                    stale_ids.append(sid)
            for sid in stale_ids:
                print(f"[SessionManager] Cleaning up stale session: {sid}")
                self.sessions[sid].shutdown()
                del self.sessions[sid]
