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

def test_create_doctor(client: TestClient):
    payload = {}
    response = client.post('/doctor', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_doctor_list(client: TestClient):
    test_create_doctor(client)
    response = client.get('/doctor')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_doctor(client: TestClient):
    for _ in range(3):
        test_create_doctor(client)
    response = client.get('/doctor?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_doctor(client: TestClient):
    item = test_create_doctor(client)
    response = client.get(f'/doctor/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_doctor(client: TestClient):
    item = test_create_doctor(client)
    # Update payload could be empty for generic test
    response = client.put(f'/doctor/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_doctor(client: TestClient):
    item = test_create_doctor(client)
    response = client.delete(f'/doctor/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/doctor/{item["id"]}')
    assert response2.status_code == 404

def test_create_appointment(client: TestClient):
    payload = {
        'patient_id': str(uuid.uuid4()),
        'doctor_id': str(uuid.uuid4())
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
