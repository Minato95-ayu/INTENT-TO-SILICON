import pytest
import uuid
from fastapi.testclient import TestClient

def test_create_patient(client: TestClient):
    payload = {}
    response = client.post('/patient', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_patient_list(client: TestClient):
    test_create_patient(client)
    response = client.get('/patient')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_patient(client: TestClient):
    for _ in range(3):
        test_create_patient(client)
    response = client.get('/patient?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_patient(client: TestClient):
    item = test_create_patient(client)
    response = client.get(f'/patient/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_patient(client: TestClient):
    item = test_create_patient(client)
    # Update payload could be empty for generic test
    response = client.put(f'/patient/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_patient(client: TestClient):
    item = test_create_patient(client)
    response = client.delete(f'/patient/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/patient/{item["id"]}')
    assert response2.status_code == 404

def test_create_appointment(client: TestClient):
    payload = {
        'patient_id': str(uuid.uuid4())
    }
    response = client.post('/appointment', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_appointment_list(client: TestClient):
    test_create_appointment(client)
    response = client.get('/appointment')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_appointment(client: TestClient):
    for _ in range(3):
        test_create_appointment(client)
    response = client.get('/appointment?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_appointment(client: TestClient):
    item = test_create_appointment(client)
    response = client.get(f'/appointment/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_appointment(client: TestClient):
    item = test_create_appointment(client)
    # Update payload could be empty for generic test
    response = client.put(f'/appointment/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_appointment(client: TestClient):
    item = test_create_appointment(client)
    response = client.delete(f'/appointment/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/appointment/{item["id"]}')
    assert response2.status_code == 404

def test_create_user(client: TestClient):
    payload = {
        'email': f"test_email_{str(uuid.uuid4())[:8]}",
        'password_hash': f"test_password_hash_{str(uuid.uuid4())[:8]}"
    }
    response = client.post('/user', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_user_list(client: TestClient):
    test_create_user(client)
    response = client.get('/user')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_user(client: TestClient):
    for _ in range(3):
        test_create_user(client)
    response = client.get('/user?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_search_case_insensitive_user(client: TestClient):
    item = test_create_user(client)
    val = str(item['email'])
    if len(val) > 2:
        search_term = val[:3].lower() + val[3:].upper()
        response = client.get(f'/user?search={search_term}')
        assert response.status_code == 200
        assert len(response.json()['items']) >= 1

def test_empty_search_user(client: TestClient):
    response = client.get('/user?search=NON_EXISTENT_IMPOSSIBLE_STRING_12345')
    assert response.status_code == 200
    assert len(response.json()['items']) == 0

def test_get_user(client: TestClient):
    item = test_create_user(client)
    response = client.get(f'/user/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_user(client: TestClient):
    item = test_create_user(client)
    # Update payload could be empty for generic test
    response = client.put(f'/user/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_user(client: TestClient):
    item = test_create_user(client)
    response = client.delete(f'/user/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/user/{item["id"]}')
    assert response2.status_code == 404

def test_create_role(client: TestClient):
    payload = {}
    response = client.post('/role', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_role_list(client: TestClient):
    test_create_role(client)
    response = client.get('/role')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_role(client: TestClient):
    for _ in range(3):
        test_create_role(client)
    response = client.get('/role?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_role(client: TestClient):
    item = test_create_role(client)
    response = client.get(f'/role/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_role(client: TestClient):
    item = test_create_role(client)
    # Update payload could be empty for generic test
    response = client.put(f'/role/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_role(client: TestClient):
    item = test_create_role(client)
    response = client.delete(f'/role/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/role/{item["id"]}')
    assert response2.status_code == 404

def test_observability_request_id(client: TestClient):
    response = client.get('/patient')
    assert response.status_code == 200
    assert 'x-request-id' in response.headers
    assert response.headers['x-request-id'] != ''

def test_audit_log_created(client: TestClient, db_session):
    from models import AuditLog
    initial_count = db_session.query(AuditLog).count()
    item = test_create_patient(client)
    assert db_session.query(AuditLog).count() > initial_count
    audit_rec = db_session.query(AuditLog).filter_by(action='create', entity_name='patient').first()
    assert audit_rec is not None
    assert audit_rec.request_id is not None

def test_event_dispatch(client: TestClient):
    from event_bus import event_bus, Event
    received_events = []
    def handler(evt: Event):
        received_events.append(evt)
    event_bus.subscribe('patient.created', handler)
    test_create_patient(client)
    import time
    time.sleep(0.1)  # wait for background task
    assert len(received_events) >= 1
    assert received_events[-1].entity == 'patient'
    assert received_events[-1].action == 'create'

def test_multiple_subscribers(client: TestClient):
    from event_bus import event_bus, Event
    counters = {'h1': 0, 'h2': 0, 'h3': 0}
    def h1(e: Event): counters['h1'] += 1
    def h2(e: Event): counters['h2'] += 1
    def h3(e: Event): counters['h3'] += 1
    event_bus.subscribe('patient.deleted', h1)
    event_bus.subscribe('patient.deleted', h2)
    event_bus.subscribe('patient.deleted', h3)
    item = test_create_patient(client)
    client.delete(f'/patient/{item["id"]}')
    import time
    time.sleep(0.1)
    assert counters['h1'] >= 1
    assert counters['h2'] >= 1
    assert counters['h3'] >= 1
