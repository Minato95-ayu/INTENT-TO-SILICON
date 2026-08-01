from aayu.runtime.base import BaseRuntime
from aayu.runtime.http.server import HTTPServerEngine
from aayu.runtime.http.router import Router
from aayu.runtime.http.middleware import MiddlewarePipeline
from aayu.runtime.http.errors import ErrorEngine
from aayu.runtime.http.security import SecurityMiddleware

class HTTPRuntime(BaseRuntime):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.server = None

    def initialize(self):
        # 1. Setup Architecture
        router = Router()
        error_engine = ErrorEngine()
        
        pipeline = MiddlewarePipeline()
        pipeline.add(SecurityMiddleware())
        
        # 2. Parse Application IR
        api_ir = self.metadata.get("api_ir", {})
        services = api_ir.get("services", [])
        
        for service in services:
            endpoints = service.get("endpoints", [])
            for ep in endpoints:
                method = ep.get("method", "GET")
                path = ep.get("path", "/")
                
                # Create a generic closure to act as the native handler
                def handler(ctx, _name=service.get("name"), _path=path):
                    ctx.response.json({
                        "status": "success",
                        "service": _name,
                        "path": _path,
                        "params": ctx.request.params,
                        "body": ctx.request.body
                    })
                
                router.add_route(method, path, handler)

        # 3. Mount Server
        self.server = HTTPServerEngine(
            port=3000, 
            router=router, 
            middleware_pipeline=pipeline, 
            error_engine=error_engine
        )

    def start(self):
        self.server.start()
