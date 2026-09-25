# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import asyncio
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
        
        class DummyRenderer:
            pass
        self.vm.renderer = DummyRenderer()
        self.vm.load(prog.bytecode, list(prog.constant_pool.values()), prog.action_addresses)
        self.vm.execute()
        self.vm.call_action_by_name("__PAGE_START__")
        
        self.last_accessed = time.time()
        self.current_tree_json = "{}"
        self.dirty = True
        
        self.message_queue = asyncio.Queue()
        self.running = True
        
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
        self.task = self.loop.create_task(self._run_loop())
        
    async def _run_loop(self):
        import json
        from runtime.renderers.web_renderer import serialize_node
        while self.running:
            try:
                if self.event_queue.has_events():
                    evt = self.event_queue.pop()
                    if evt.__class__.__name__ == "ActionEvent":
                        await asyncio.to_thread(self.vm.call_action_by_name, evt.action_name)
                    elif evt.__class__.__name__ == "InputEvent":
                        await asyncio.to_thread(self.vm.update_state, evt.target_state, evt.value)
                        
                    if self.vm.router.current_route:
                        await asyncio.to_thread(self.vm.call_action_by_name, self.vm.router.current_route.name)
                    else:
                        await asyncio.to_thread(self.vm.call_action_by_name, "__PAGE_START__")
                    self.dirty = True
                
                if self.dirty:
                    if self.vm.interpreter.render_tree and self.vm.interpreter.render_tree.root:
                        style_sheet = set()
                        tree_dict = await asyncio.to_thread(serialize_node, self.vm.interpreter.render_tree.root, style_sheet)
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
                            except asyncio.QueueFull:
                                pass
                    self.dirty = False
                            
                await asyncio.sleep(0.016)
            except asyncio.CancelledError:
                break
            except Exception as e:
                import traceback
                print(f"[DEBUG ASYNC] EXCEPTION IN RUN LOOP: {e}")
                traceback.print_exc()
            
    def touch(self):
        self.last_accessed = time.time()
        
    def shutdown(self):
        self.running = False
        if hasattr(self, 'task'):
            self.task.cancel()

class SessionManager:
    def __init__(self, prog: Any, session_timeout: int = 3600):
        self.prog = prog
        self.session_timeout = session_timeout
        self.sessions: Dict[str, Session] = {}
        
    def get_or_create_session(self, session_id: str) -> Session:
        if not session_id or session_id not in self.sessions:
            session_id = str(uuid.uuid4())
            try:
                self.sessions[session_id] = Session(session_id, self.prog)
                print(f"[SessionManager] Created new async session: {session_id}")
            except Exception as e:
                import traceback
                print(f"[SessionManager] ERROR creating session: {e}")
                traceback.print_exc()
                raise e
        
        session = self.sessions[session_id]
        session.touch()
        return session
            
    def get_session(self, session_id: str) -> Session:
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.touch()
            return session
        return None
            
    def cleanup_stale_sessions(self):
        now = time.time()
        stale_ids = [sid for sid, sess in self.sessions.items() if now - sess.last_accessed > self.session_timeout]
        for sid in stale_ids:
            self.sessions[sid].shutdown()
            del self.sessions[sid]
