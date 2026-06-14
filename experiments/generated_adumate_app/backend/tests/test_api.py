import pytest
import uuid
from fastapi.testclient import TestClient

def test_create_course(client: TestClient):
    payload = {}
    response = client.post('/course', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_course_list(client: TestClient):
    test_create_course(client)
    response = client.get('/course')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_course(client: TestClient):
    for _ in range(3):
        test_create_course(client)
    response = client.get('/course?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_course(client: TestClient):
    item = test_create_course(client)
    response = client.get(f'/course/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_course(client: TestClient):
    item = test_create_course(client)
    # Update payload could be empty for generic test
    response = client.put(f'/course/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_course(client: TestClient):
    item = test_create_course(client)
    response = client.delete(f'/course/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/course/{item["id"]}')
    assert response2.status_code == 404

def test_create_room_allocation(client: TestClient):
    payload = {
        'student_id': str(uuid.uuid4())
    }
    response = client.post('/room_allocation', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_room_allocation_list(client: TestClient):
    test_create_room_allocation(client)
    response = client.get('/room_allocation')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_room_allocation(client: TestClient):
    for _ in range(3):
        test_create_room_allocation(client)
    response = client.get('/room_allocation?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_room_allocation(client: TestClient):
    item = test_create_room_allocation(client)
    response = client.get(f'/room_allocation/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_room_allocation(client: TestClient):
    item = test_create_room_allocation(client)
    # Update payload could be empty for generic test
    response = client.put(f'/room_allocation/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_room_allocation(client: TestClient):
    item = test_create_room_allocation(client)
    response = client.delete(f'/room_allocation/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/room_allocation/{item["id"]}')
    assert response2.status_code == 404

def test_create_student(client: TestClient):
    payload = {}
    response = client.post('/student', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_student_list(client: TestClient):
    test_create_student(client)
    response = client.get('/student')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_student(client: TestClient):
    for _ in range(3):
        test_create_student(client)
    response = client.get('/student?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_student(client: TestClient):
    item = test_create_student(client)
    response = client.get(f'/student/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_student(client: TestClient):
    item = test_create_student(client)
    # Update payload could be empty for generic test
    response = client.put(f'/student/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_student(client: TestClient):
    item = test_create_student(client)
    response = client.delete(f'/student/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/student/{item["id"]}')
    assert response2.status_code == 404

def test_create_student_course(client: TestClient):
    payload = {
        'student_id': str(uuid.uuid4()),
        'course_id': str(uuid.uuid4())
    }
    response = client.post('/student_course', json=payload)
    assert response.status_code == 200
    assert 'student_id' in response.json()
    return response.json()

def test_get_student_course_list(client: TestClient):
    test_create_student_course(client)
    response = client.get('/student_course')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_student_course(client: TestClient):
    for _ in range(3):
        test_create_student_course(client)
    response = client.get('/student_course?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_student_course(client: TestClient):
    item = test_create_student_course(client)
    response = client.get(f'/student_course/{item["student_id"]}')
    assert response.status_code == 200
    assert response.json()['student_id'] == item['student_id']

def test_update_student_course(client: TestClient):
    item = test_create_student_course(client)
    # Update payload could be empty for generic test
    response = client.put(f'/student_course/{item["student_id"]}', json={})
    assert response.status_code == 200
    assert response.json()['student_id'] == item['student_id']

def test_delete_student_course(client: TestClient):
    item = test_create_student_course(client)
    response = client.delete(f'/student_course/{item["student_id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/student_course/{item["student_id"]}')
    assert response2.status_code == 404

def test_observability_request_id(client: TestClient):
    response = client.get('/course')
    assert response.status_code == 200
    assert 'x-request-id' in response.headers
    assert response.headers['x-request-id'] != ''

def test_audit_log_created(client: TestClient, db_session):
    from models import AuditLog
    initial_count = db_session.query(AuditLog).count()
    item = test_create_course(client)
    assert db_session.query(AuditLog).count() > initial_count
    audit_rec = db_session.query(AuditLog).filter_by(action='create', entity_name='course').first()
    assert audit_rec is not None
    assert audit_rec.request_id is not None
