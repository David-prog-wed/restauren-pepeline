import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from app.main import app, users_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    users_db.clear()
    with app.test_client() as c:
        yield c

def test_health_check(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_register_user(client):
    r = client.post("/api/auth/register",
        json={"name": "Carlos Perez", "email": "carlos@test.com", "password": "segura123"})
    assert r.status_code == 201
    assert "exitosamente" in r.get_json()["message"]

def test_register_duplicate(client):
    client.post("/api/auth/register",
        json={"name": "Ana", "email": "ana@test.com", "password": "pass"})
    r = client.post("/api/auth/register",
        json={"name": "Ana", "email": "ana@test.com", "password": "pass"})
    assert r.status_code == 409

def test_login_success(client):
    client.post("/api/auth/register",
        json={"name": "Luis", "email": "luis@test.com", "password": "abc123"})
    r = client.post("/api/auth/login",
        json={"email": "luis@test.com", "password": "abc123"})
    assert r.status_code == 200
    assert "token" in r.get_json()

def test_login_invalid(client):
    r = client.post("/api/auth/login",
        json={"email": "nadie@test.com", "password": "wrong"})
    assert r.status_code == 401

def test_register_missing_fields(client):
    r = client.post("/api/auth/register", json={"email": "solo@test.com"})
    assert r.status_code == 400
