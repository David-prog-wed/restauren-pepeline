import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from app.main import app, orders_db, calculate_total

@pytest.fixture
def client():
    app.config["TESTING"] = True
    orders_db.clear()
    with app.test_client() as c:
        yield c

def test_health_check(client):
    r = client.get("/health")
    assert r.status_code == 200

def test_get_menu(client):
    r = client.get("/api/menu/")
    assert r.status_code == 200
    assert r.get_json()["total_items"] == 5

def test_calculate_total():
    result = calculate_total([
        {"product_id": "P001", "quantity": 1},
        {"product_id": "P004", "quantity": 2}
    ])
    assert result is not None
    assert result["subtotal"] == 48000
    assert result["total"] == 48000 + round(48000 * 0.08)

def test_create_order_success(client):
    r = client.post("/api/orders/", json={
        "customer_id": 1,
        "items": [{"product_id": "P001", "quantity": 1}]
    })
    assert r.status_code == 201
    assert r.get_json()["status"] == "pending"

def test_create_order_invalid_product(client):
    r = client.post("/api/orders/", json={
        "customer_id": 1,
        "items": [{"product_id": "NOPE", "quantity": 1}]
    })
    assert r.status_code == 404

def test_create_order_missing_fields(client):
    r = client.post("/api/orders/", json={"customer_id": 1})
    assert r.status_code == 400

def test_confirm_order(client):
    cr = client.post("/api/orders/", json={
        "customer_id": 2,
        "items": [{"product_id": "P002", "quantity": 1}]
    })
    oid = cr.get_json()["id"]
    r = client.put(f"/api/orders/{oid}/confirm")
    assert r.status_code == 200
    assert r.get_json()["order"]["status"] == "confirmed"
