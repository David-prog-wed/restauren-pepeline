import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from app.main import app, reservations_db, check_availability

@pytest.fixture
def client():
    app.config["TESTING"] = True
    reservations_db.clear()
    with app.test_client() as c:
        yield c

def test_health_check(client):
    r = client.get("/health")
    assert r.status_code == 200

def test_check_availability_empty():
    reservations_db.clear()
    result = check_availability("2026-06-01", "19:00", 2)
    assert result["available_tables"] == 5

def test_create_reservation_success(client):
    r = client.post("/api/reservations/", json={
        "date": "2026-06-01", "time": "19:00",
        "party_size": 2, "customer_id": 101})
    assert r.status_code == 201
    assert r.get_json()["status"] == "confirmed"

def test_create_reservation_missing_fields(client):
    r = client.post("/api/reservations/", json={"date": "2026-06-01"})
    assert r.status_code == 400

def test_cancel_reservation(client):
    cr = client.post("/api/reservations/", json={
        "date": "2026-06-02", "time": "18:00",
        "party_size": 2, "customer_id": 202})
    rid = cr.get_json()["id"]
    r = client.put(f"/api/reservations/{rid}/cancel")
    assert r.status_code == 200
    assert r.get_json()["reservation"]["status"] == "cancelled"

def test_get_reservation_not_found(client):
    r = client.get("/api/reservations/notexists")
    assert r.status_code == 404

def test_availability_ignores_cancelled(client):
    cr = client.post("/api/reservations/", json={
        "date": "2026-06-10", "time": "20:00",
        "party_size": 2, "customer_id": 303})
    rid = cr.get_json()["id"]
    client.put(f"/api/reservations/{rid}/cancel")
    result = check_availability("2026-06-10", "20:00", 2)
    assert result["available_tables"] == 5
