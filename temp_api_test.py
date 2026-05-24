import json
import urllib.request
import urllib.error


def post(url: str, payload: dict):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def put(url: str):
    req = urllib.request.Request(url, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def get(url: str):
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def main():
    # AUTH
    auth = "http://localhost:5001"
    s, b = post(
        f"{auth}/api/auth/register",
        {"name": "Test User", "email": "testuser@example.com", "password": "abc123"},
    )
    print("AUTH_REGISTER:", s, b)

    s, b = post(
        f"{auth}/api/auth/login",
        {"email": "testuser@example.com", "password": "abc123"},
    )
    print("AUTH_LOGIN_OK:", s, b)

    s, b = post(
        f"{auth}/api/auth/login",
        {"email": "testuser@example.com", "password": "wrong"},
    )
    print("AUTH_LOGIN_BAD:", s, b)

    # RESERVATIONS
    res = "http://localhost:5002"
    s, b = get(f"{res}/api/reservations/availability?date=2026-06-15&time=19:00&party_size=2")
    print("RES_AVAIL:", s, b)

    s, b = post(
        f"{res}/api/reservations/",
        {"date": "2026-06-15", "time": "19:00", "party_size": 2, "customer_id": 1},
    )
    print("RES_CREATE:", s, b)

    reservation_id = None
    try:
        reservation_id = json.loads(b).get("id")
    except Exception:
        reservation_id = None

    if reservation_id:
        s, b = get(f"{res}/api/reservations/{reservation_id}")
        print("RES_GET:", s, b)

        s, b = put(f"{res}/api/reservations/{reservation_id}/cancel")
        print("RES_CANCEL:", s, b)

    s, b = get(f"{res}/api/reservations/notexists")
    print("RES_GET_404:", s, b)

    # ORDERS
    ords = "http://localhost:5003"
    s, b = get(f"{ords}/api/menu/")
    print("ORD_MENU:", s, b)

    s, b = post(
        f"{ords}/api/orders/",
        {"customer_id": 2, "items": [{"product_id": "P001", "quantity": 1}]},
    )
    print("ORD_CREATE:", s, b)

    order_id = None
    try:
        order_id = json.loads(b).get("id")
    except Exception:
        order_id = None

    if order_id:
        s, b = put(f"{ords}/api/orders/{order_id}/confirm")
        print("ORD_CONFIRM:", s, b)

        s, b = get(f"{ords}/api/orders/{order_id}")
        print("ORD_GET:", s, b)

    s, b = post(
        f"{ords}/api/orders/",
        {"customer_id": 2, "items": [{"product_id": "PX99", "quantity": 1}]},
    )
    print("ORD_CREATE_BAD_PRODUCT:", s, b)


if __name__ == "__main__":
    main()
