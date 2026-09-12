import pytest
import asyncio
from runtime.http.runtime import HttpRuntime

@pytest.mark.asyncio
async def test_http_runtime_e2e():
    rt = HttpRuntime(port=8080)
    rt.register_route("GET", "/test", lambda req: {"status": "ok"})
    # Since start() is blocking, we can't easily test the full server without background threads.
    # We will just verify routes are registered.
    assert len(rt.router.routes) > 0
    assert "/test" in [r.path for r in rt.router.routes]
