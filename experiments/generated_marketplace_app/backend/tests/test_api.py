import pytest
import uuid
from fastapi.testclient import TestClient

def test_create_product(client: TestClient):
    payload = {}
    response = client.post('/product', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_product_list(client: TestClient):
    test_create_product(client)
    response = client.get('/product')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_product(client: TestClient):
    for _ in range(3):
        test_create_product(client)
    response = client.get('/product?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_product(client: TestClient):
    item = test_create_product(client)
    response = client.get(f'/product/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_product(client: TestClient):
    item = test_create_product(client)
    # Update payload could be empty for generic test
    response = client.put(f'/product/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_product(client: TestClient):
    item = test_create_product(client)
    response = client.delete(f'/product/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/product/{item["id"]}')
    assert response2.status_code == 404

def test_create_order(client: TestClient):
    payload = {}
    response = client.post('/order', json=payload)
    assert response.status_code == 200
    assert 'id' in response.json()
    return response.json()

def test_get_order_list(client: TestClient):
    test_create_order(client)
    response = client.get('/order')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_order(client: TestClient):
    for _ in range(3):
        test_create_order(client)
    response = client.get('/order?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_order(client: TestClient):
    item = test_create_order(client)
    response = client.get(f'/order/{item["id"]}')
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_update_order(client: TestClient):
    item = test_create_order(client)
    # Update payload could be empty for generic test
    response = client.put(f'/order/{item["id"]}', json={})
    assert response.status_code == 200
    assert response.json()['id'] == item['id']

def test_delete_order(client: TestClient):
    item = test_create_order(client)
    response = client.delete(f'/order/{item["id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/order/{item["id"]}')
    assert response2.status_code == 404

def test_create_product_order(client: TestClient):
    payload = {
        'product_id': str(uuid.uuid4()),
        'order_id': str(uuid.uuid4())
    }
    response = client.post('/product_order', json=payload)
    assert response.status_code == 200
    assert 'product_id' in response.json()
    return response.json()

def test_get_product_order_list(client: TestClient):
    test_create_product_order(client)
    response = client.get('/product_order')
    assert response.status_code == 200
    assert len(response.json()['items']) >= 1
    assert response.json()['page'] == 1
    assert response.json()['size'] == 20

def test_pagination_product_order(client: TestClient):
    for _ in range(3):
        test_create_product_order(client)
    response = client.get('/product_order?page=1&size=2')
    assert response.status_code == 200
    assert len(response.json()['items']) <= 2
    assert response.json()['size'] == 2

def test_get_product_order(client: TestClient):
    item = test_create_product_order(client)
    response = client.get(f'/product_order/{item["product_id"]}')
    assert response.status_code == 200
    assert response.json()['product_id'] == item['product_id']

def test_update_product_order(client: TestClient):
    item = test_create_product_order(client)
    # Update payload could be empty for generic test
    response = client.put(f'/product_order/{item["product_id"]}', json={})
    assert response.status_code == 200
    assert response.json()['product_id'] == item['product_id']

def test_delete_product_order(client: TestClient):
    item = test_create_product_order(client)
    response = client.delete(f'/product_order/{item["product_id"]}')
    assert response.status_code == 200
    # Verify deleted
    response2 = client.get(f'/product_order/{item["product_id"]}')
    assert response2.status_code == 404
