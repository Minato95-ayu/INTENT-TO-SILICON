import asyncio
from runtime.renderers.web_renderer import WebRenderer
class DummySessionManager:
    def get_or_create_session(self, id):
        class DummySession:
            session_id = "test"
            current_tree_json = "{}"
        return DummySession()

async def test():
    renderer = WebRenderer(DummySessionManager())
    renderer.start()
    
    scope = {'type': 'http', 'path': '/'}
    
    async def receive():
        return {}
    
    async def send(msg):
        print("SEND:", msg)
        
    try:
        await renderer.asgi_app(scope, receive, send)
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(test())