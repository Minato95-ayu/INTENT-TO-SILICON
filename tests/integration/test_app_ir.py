import pytest
from aayu.compiler.backend.app_ir import AppIR, DatabaseIR, FrontendIR, RouteIR

def test_app_ir_models():
    db = DatabaseIR("sqlite", [{"name": "User", "fields": []}])
    fe = FrontendIR("react", [])
    routes = [RouteIR("GET", "/test", "handler")]
    
    app = AppIR("test_app", "test desc", db, fe, routes)
    
    assert app.name == "test_app"
    assert app.database.provider == "sqlite"
    assert app.frontend.framework == "react"
    assert app.backend_routes[0].method == "GET"
