"""
Aayu Testing Generator (Sprint 34)

Generates automated integration tests for the FastAPI application.
Generates a tests/ directory containing:
- conftest.py (fixtures)
- test_main.py (health check)
- test_api.py (CRUD for all entities)
- test_auth.py (Auth endpoints, if applicable)
"""

from typing import Dict
from .schema_nodes import SchemaModel, Table, Column

class TestGenerator:
    def __init__(self):
        pass

    def generate(self, schema: SchemaModel) -> Dict[str, str]:
        files = {}
        files["tests/conftest.py"] = self._gen_conftest(schema)
        files["tests/test_main.py"] = self._gen_test_main()
        files["tests/test_api.py"] = self._gen_test_api(schema)
        
        if getattr(schema, 'has_auth', False):
            files["tests/test_auth.py"] = self._gen_test_auth()
            
        return files

    def _gen_conftest(self, schema: SchemaModel) -> str:
        lines = [
            "import pytest",
            "import sys",
            "import os",
            "import uuid",
            "sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))",
            "",
            "from fastapi.testclient import TestClient",
            "from sqlalchemy import create_engine",
            "from sqlalchemy.orm import sessionmaker",
            "from sqlalchemy.pool import StaticPool",
            "",
            "from main import app",
            "from database import Base, get_db",
            "",
            "# Use in-memory SQLite database for testing",
            "SQLALCHEMY_DATABASE_URL = \"sqlite:///:memory:\"",
            "",
            "engine = create_engine(",
            "    SQLALCHEMY_DATABASE_URL,",
            "    connect_args={\"check_same_thread\": False},",
            "    poolclass=StaticPool,",
            ")",
            "TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)",
            "",
            "@pytest.fixture(scope=\"function\")",
            "def db_session():",
            "    Base.metadata.create_all(bind=engine)",
            "    db = TestingSessionLocal()",
            "    try:",
            "        yield db",
            "    finally:",
            "        db.close()",
            "        Base.metadata.drop_all(bind=engine)",
            "",
            "@pytest.fixture(scope=\"function\")",
            "def client(db_session):",
            "    def override_get_db():",
            "        try:",
            "            yield db_session",
            "        finally:",
            "            pass",
            "            ",
            "    app.dependency_overrides[get_db] = override_get_db",
            "    with TestClient(app) as c:",
            "        yield c",
            "    app.dependency_overrides.clear()",
            ""
        ]
        
        if getattr(schema, 'has_rbac', False):
            lines.extend([
                "@pytest.fixture(scope=\"function\")",
                "def admin_client(client, db_session):",
                "    from models import User, Role, Permission, UserRole, RolePermission",
                "    from auth import get_password_hash, create_access_token",
                "    ",
                "    # Create permissions",
                "    p_read = Permission(id=str(uuid.uuid4()), name='read')",
                "    p_create = Permission(id=str(uuid.uuid4()), name='create')",
                "    p_update = Permission(id=str(uuid.uuid4()), name='update')",
                "    p_delete = Permission(id=str(uuid.uuid4()), name='delete')",
                "    ",
                "    # Create admin role",
                "    r_admin = Role(id=str(uuid.uuid4()), name='admin')",
                "    ",
                "    # Create admin user",
                "    u_admin = User(id=str(uuid.uuid4()), email='admin@test.com', password_hash=get_password_hash('adminpass'))",
                "    ",
                "    db_session.add_all([p_read, p_create, p_update, p_delete, r_admin, u_admin])",
                "    db_session.commit()",
                "    ",
                "    # Link permission to role",
                "    db_session.add_all([",
                "        RolePermission(role_id=r_admin.id, permission_id=p_read.id),",
                "        RolePermission(role_id=r_admin.id, permission_id=p_create.id),",
                "        RolePermission(role_id=r_admin.id, permission_id=p_update.id),",
                "        RolePermission(role_id=r_admin.id, permission_id=p_delete.id)",
                "    ])",
                "    ",
                "    # Link role to user",
                "    db_session.add(UserRole(user_id=u_admin.id, role_id=r_admin.id))",
                "    db_session.commit()",
                "    ",
                "    # Generate token",
                "    access_token = create_access_token(data={\"sub\": u_admin.email})",
                "    client.headers.update({\"Authorization\": f\"Bearer {access_token}\"})",
                "    return client",
                ""
            ])
            
        return "\n".join(lines)

    def _gen_test_main(self) -> str:
        return """from fastapi.testclient import TestClient

def test_health_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
"""

    def _get_fake_value_for_column(self, col: Column) -> str:
        if col.type.upper() == "UUID":
            return 'str(uuid.uuid4())'
        elif col.type.upper() == "INTEGER":
            return '123'
        elif col.type.upper() == "BOOLEAN":
            return 'True'
        else:
            return f'f"test_{col.name}_{{str(uuid.uuid4())[:8]}}"'

    def _gen_test_api(self, schema: SchemaModel) -> str:
        lines = [
            "import pytest",
            "import uuid",
            "from fastapi.testclient import TestClient",
            ""
        ]
        
        client_fixture = "admin_client" if getattr(schema, 'has_rbac', False) else "client"
        
        for table in schema.tables:
            if getattr(table, 'is_system', False):
                continue
                
            # Skip testing junction tables or auth internal tables directly if they are just infrastructure
            if table.name in ["role", "permission", "user_role", "role_permission"] and getattr(schema, 'has_rbac', False):
                continue
                
            route = table.name
            
            # Generate fake payload
            payload_lines = []
            for col in table.columns:
                if col.name != "id":
                    val = self._get_fake_value_for_column(col)
                    payload_lines.append(f"        '{col.name}': {val}")
                    
            if not payload_lines:
                payload_str = "{}"
            else:
                payload_str = "{\n" + ",\n".join(payload_lines) + "\n    }"
            
            has_id = any(c.name == 'id' for c in table.columns)
            id_field = 'id' if has_id else table.columns[0].name

            # test create
            lines.append(f"def test_create_{route}({client_fixture}: TestClient):")
            lines.append(f"    payload = {payload_str}")
            lines.append(f"    response = {client_fixture}.post('/{route}', json=payload)")
            lines.append(f"    assert response.status_code == 200")
            lines.append(f"    assert '{id_field}' in response.json()")
            lines.append(f"    return response.json()")
            lines.append("")
            
            # test get list
            lines.append(f"def test_get_{route}_list({client_fixture}: TestClient):")
            lines.append(f"    test_create_{route}({client_fixture})")
            lines.append(f"    response = {client_fixture}.get('/{route}')")
            lines.append(f"    assert response.status_code == 200")
            lines.append(f"    assert len(response.json()['items']) >= 1")
            lines.append(f"    assert response.json()['page'] == 1")
            lines.append(f"    assert response.json()['size'] == 20")
            lines.append("")
            
            # test pagination
            lines.append(f"def test_pagination_{route}({client_fixture}: TestClient):")
            lines.append(f"    for _ in range(3):")
            lines.append(f"        test_create_{route}({client_fixture})")
            lines.append(f"    response = {client_fixture}.get('/{route}?page=1&size=2')")
            lines.append(f"    assert response.status_code == 200")
            lines.append(f"    assert len(response.json()['items']) <= 2")
            lines.append(f"    assert response.json()['size'] == 2")
            lines.append("")
            
            # test search (case-insensitive) and empty search
            if getattr(table, 'searchable_columns', []):
                lines.append(f"def test_search_case_insensitive_{route}({client_fixture}: TestClient):")
                lines.append(f"    item = test_create_{route}({client_fixture})")
                search_col = table.searchable_columns[0].name
                lines.append(f"    val = str(item['{search_col}'])")
                lines.append(f"    if len(val) > 2:")
                lines.append(f"        search_term = val[:3].lower() + val[3:].upper()")
                lines.append(f"        response = {client_fixture}.get(f'/{route}?search={{search_term}}')")
                lines.append(f"        assert response.status_code == 200")
                lines.append(f"        assert len(response.json()['items']) >= 1")
                lines.append("")
                
                lines.append(f"def test_empty_search_{route}({client_fixture}: TestClient):")
                lines.append(f"    response = {client_fixture}.get('/{route}?search=NON_EXISTENT_IMPOSSIBLE_STRING_12345')")
                lines.append(f"    assert response.status_code == 200")
                lines.append(f"    assert len(response.json()['items']) == 0")
                lines.append("")
            
            # test get single
            lines.append(f"def test_get_{route}({client_fixture}: TestClient):")
            lines.append(f"    item = test_create_{route}({client_fixture})")
            lines.append(f"    response = {client_fixture}.get(f'/{route}/{{item[\"{id_field}\"]}}')")
            lines.append(f"    assert response.status_code == 200")
            lines.append(f"    assert response.json()['{id_field}'] == item['{id_field}']")
            lines.append("")
            
            # test update
            lines.append(f"def test_update_{route}({client_fixture}: TestClient):")
            lines.append(f"    item = test_create_{route}({client_fixture})")
            lines.append(f"    # Update payload could be empty for generic test")
            lines.append(f"    response = {client_fixture}.put(f'/{route}/{{item[\"{id_field}\"]}}', json={{}})")
            lines.append(f"    assert response.status_code == 200")
            lines.append(f"    assert response.json()['{id_field}'] == item['{id_field}']")
            lines.append("")
            
            # test delete
            lines.append(f"def test_delete_{route}({client_fixture}: TestClient):")
            lines.append(f"    item = test_create_{route}({client_fixture})")
            lines.append(f"    response = {client_fixture}.delete(f'/{route}/{{item[\"{id_field}\"]}}')")
            lines.append(f"    assert response.status_code == 200")
            lines.append(f"    # Verify deleted")
            lines.append(f"    response2 = {client_fixture}.get(f'/{route}/{{item[\"{id_field}\"]}}')")
            lines.append(f"    assert response2.status_code == 404")
            lines.append("")
            
        # Observability Tests
        has_audit = any(t.name == 'audit_log' for t in schema.tables)
        test_target = None
        for t in schema.tables:
            if not getattr(t, 'is_system', False) and t.name not in ["role", "permission", "user_role", "role_permission"]:
                test_target = t.name
                break
                
        if test_target:
            lines.extend([
                f"def test_observability_request_id({client_fixture}: TestClient):",
                f"    response = {client_fixture}.get('/{test_target}')",
                "    assert response.status_code == 200",
                "    assert 'x-request-id' in response.headers",
                "    assert response.headers['x-request-id'] != ''",
                ""
            ])
            if has_audit:
                lines.extend([
                    f"def test_audit_log_created({client_fixture}: TestClient, db_session):",
                    "    from models import AuditLog",
                    "    initial_count = db_session.query(AuditLog).count()",
                    f"    item = test_create_{test_target}({client_fixture})",
                    "    assert db_session.query(AuditLog).count() > initial_count",
                    f"    audit_rec = db_session.query(AuditLog).filter_by(action='create', entity_name='{test_target}').first()",
                    "    assert audit_rec is not None",
                    "    assert audit_rec.request_id is not None",
                    ""
                ])

            # Event tests
            target_table = next(t for t in schema.tables if t.name == test_target)
            target_id_field = 'id' if any(c.name == 'id' for c in target_table.columns) else target_table.columns[0].name
            
            lines.extend([
                f"def test_event_dispatch({client_fixture}: TestClient):",
                "    from event_bus import event_bus, Event",
                "    received_events = []",
                "    def handler(evt: Event):",
                "        received_events.append(evt)",
                f"    event_bus.subscribe('{test_target}.created', handler)",
                f"    test_create_{test_target}({client_fixture})",
                "    import time",
                "    time.sleep(0.1)  # wait for background task",
                "    assert len(received_events) >= 1",
                f"    assert received_events[-1].entity == '{test_target}'",
                "    assert received_events[-1].action == 'create'",
                "",
                f"def test_multiple_subscribers({client_fixture}: TestClient):",
                "    from event_bus import event_bus, Event",
                "    counters = {'h1': 0, 'h2': 0, 'h3': 0}",
                "    def h1(e: Event): counters['h1'] += 1",
                "    def h2(e: Event): counters['h2'] += 1",
                "    def h3(e: Event): counters['h3'] += 1",
                f"    event_bus.subscribe('{test_target}.deleted', h1)",
                f"    event_bus.subscribe('{test_target}.deleted', h2)",
                f"    event_bus.subscribe('{test_target}.deleted', h3)",
                f"    item = test_create_{test_target}({client_fixture})",
                f"    {client_fixture}.delete(f'/{test_target}/{{item[\"{target_id_field}\"]}}')",
                "    import time",
                "    time.sleep(0.1)",
                "    assert counters['h1'] >= 1",
                "    assert counters['h2'] >= 1",
                "    assert counters['h3'] >= 1",
                ""
            ])

        if getattr(schema, 'has_rbac', False) and test_target:
            lines.extend([
                "def test_rbac_unauthorized(client: TestClient):",
                f"    response = client.delete('/{test_target}/123')",
                "    assert response.status_code == 401",
                "",
                "def test_rbac_forbidden(client: TestClient, db_session):",
                "    from auth import create_access_token, get_password_hash",
                "    from models import User",
                "    u_basic = User(id=str(uuid.uuid4()), email='basic@test.com', password_hash=get_password_hash('basicpass'))",
                "    db_session.add(u_basic)",
                "    db_session.commit()",
                "    access_token = create_access_token(data={\"sub\": u_basic.email})",
                "    client.headers.update({\"Authorization\": f\"Bearer {access_token}\"})",
                f"    response = client.delete('/{test_target}/123')",
                "    assert response.status_code == 403",
                ""
            ])
            
        return "\n".join(lines)

    def _gen_test_auth(self) -> str:
        return """import pytest
import uuid
from fastapi.testclient import TestClient

def test_register(client: TestClient):
    payload = {
        "email": f"test_{uuid.uuid4()}@example.com",
        "password": "strongpassword123"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    return payload

def test_duplicate_register(client: TestClient):
    payload = test_register(client)
    # Trying to register again with same email
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400

def test_login(client: TestClient):
    payload = test_register(client)
    # Login with correct credentials
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid(client: TestClient):
    payload = test_register(client)
    payload["password"] = "wrongpassword"
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
"""
