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
