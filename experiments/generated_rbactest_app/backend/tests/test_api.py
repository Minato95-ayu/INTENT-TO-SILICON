import pytest
import uuid
from fastapi.testclient import TestClient

def test_create_patient(admin_client: TestClient):
    payload = {}
    response = admin_client.post('/patient', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_patient_list(admin_client: TestClient):
    test_create_patient(admin_client)
    response = admin_client.get('/patient')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_patient(admin_client: TestClient):
    for _ in range(3):
        test_create_patient(admin_client)
    response = admin_client.get('/patient?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_patient(admin_client: TestClient):
    item = test_create_patient(admin_client)
    response = admin_client.get(f'/patient/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_patient(admin_client: TestClient):
    item = test_create_patient(admin_client)
    # Update payload could be empty for generic test
    response = admin_client.put(f'/patient/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_patient(admin_client: TestClient):
    item = test_create_patient(admin_client)
    response = admin_client.delete(f'/patient/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = admin_client.get(f'/patient/{item["id"]}')
    assert response2.status_code == 404

def test_create_appointment(admin_client: TestClient):
    payload = {
        'patient_id': str(uuid.uuid4())
    }
    response = admin_client.post('/appointment', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_appointment_list(admin_client: TestClient):
    test_create_appointment(admin_client)
    response = admin_client.get('/appointment')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_appointment(admin_client: TestClient):
    for _ in range(3):
        test_create_appointment(admin_client)
    response = admin_client.get('/appointment?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_appointment(admin_client: TestClient):
    item = test_create_appointment(admin_client)
    response = admin_client.get(f'/appointment/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_appointment(admin_client: TestClient):
    item = test_create_appointment(admin_client)
    # Update payload could be empty for generic test
    response = admin_client.put(f'/appointment/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_appointment(admin_client: TestClient):
    item = test_create_appointment(admin_client)
    response = admin_client.delete(f'/appointment/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = admin_client.get(f'/appointment/{item["id"]}')
    assert response2.status_code == 404

def test_create_user(admin_client: TestClient):
    payload = {
        'email': f"test_email_{str(uuid.uuid4())[:8]}",
        'password_hash': f"test_password_hash_{str(uuid.uuid4())[:8]}"
    }
    response = admin_client.post('/user', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_user_list(admin_client: TestClient):
    test_create_user(admin_client)
    response = admin_client.get('/user')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_user(admin_client: TestClient):
    for _ in range(3):
        test_create_user(admin_client)
    response = admin_client.get('/user?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_search_case_insensitive_user(admin_client: TestClient):
    item = test_create_user(admin_client)
    val = str(item['email'])
    if len(val) > 2:
        search_term = val[:3].lower() + val[3:].upper()
        response = admin_client.get(f'/user?search={search_term}')
        assert response.status_code == 200
        assert len(response.json()['items']) >= 1

def test_empty_search_user(admin_client: TestClient):
    response = admin_client.get('/user?search=NON_EXISTENT_IMPOSSIBLE_STRING_12345')
    assert response.status_code == 200
    assert len(response.json()['items']) == 0

def test_get_user(admin_client: TestClient):
    item = test_create_user(admin_client)
    response = admin_client.get(f'/user/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_user(admin_client: TestClient):
    item = test_create_user(admin_client)
    # Update payload could be empty for generic test
    response = admin_client.put(f'/user/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_user(admin_client: TestClient):
    item = test_create_user(admin_client)
    response = admin_client.delete(f'/user/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = admin_client.get(f'/user/{item["id"]}')
    assert response2.status_code == 404

def test_observability_request_id(admin_client: TestClient):
    response = admin_client.get('/patient')
    assert response.status_code == 200
    assert 'x-request-id' in response.headers
    assert response.headers['x-request-id'] != ''

def test_audit_log_created(admin_client: TestClient, db_session):
    from models import AuditLog
    initial_count = db_session.query(AuditLog).count()
    item = test_create_patient(admin_client)
    assert db_session.query(AuditLog).count() > initial_count
    audit_rec = db_session.query(AuditLog).filter_by(action='create', entity_name='patient').first()
    assert audit_rec is not None
    assert audit_rec.request_id is not None

def test_event_dispatch(admin_client: TestClient):
    from event_bus import event_bus, Event
    received_events = []
    def handler(evt: Event):
        received_events.append(evt)
    event_bus.subscribe('patient.created', handler)
    test_create_patient(admin_client)
    import time
    time.sleep(0.1)  # wait for background task
    assert len(received_events) >= 1
    assert received_events[-1].entity == 'patient'
    assert received_events[-1].action == 'create'

def test_multiple_subscribers(admin_client: TestClient):
    from event_bus import event_bus, Event
    counters = {'h1': 0, 'h2': 0, 'h3': 0}
    def h1(e: Event): counters['h1'] += 1
    def h2(e: Event): counters['h2'] += 1
    def h3(e: Event): counters['h3'] += 1
    event_bus.subscribe('patient.deleted', h1)
    event_bus.subscribe('patient.deleted', h2)
    event_bus.subscribe('patient.deleted', h3)
    item = test_create_patient(admin_client)
    admin_client.delete(f'/patient/{item["id"]}')
    import time
    time.sleep(0.1)
    assert counters['h1'] >= 1
    assert counters['h2'] >= 1
    assert counters['h3'] >= 1

def test_rbac_unauthorized(client: TestClient):
    response = client.delete('/patient/123')
    assert response.status_code == 401

def test_rbac_forbidden(client: TestClient, db_session):
    from auth import create_access_token, get_password_hash
    from models import User
    u_basic = User(id=str(uuid.uuid4()), email='basic@test.com', password_hash=get_password_hash('basicpass'))
    db_session.add(u_basic)
    db_session.commit()
    access_token = create_access_token(data={"sub": u_basic.email})
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    response = client.delete('/patient/123')
    assert response.status_code == 403
