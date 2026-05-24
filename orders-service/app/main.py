from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
orders_db = []
MENU = {
    "P001": {"name": "Bandeja Paisa", "price": 32000},
    "P002": {"name": "Ajiaco Santafereno", "price": 28000},
    "P003": {"name": "Empanadas x3", "price": 12000},
    "P004": {"name": "Jugo Natural", "price": 8000},
    "P005": {"name": "Postre del dia", "price": 9000},
}

def calculate_total(items):
    subtotal, order_items = 0, []
    for item in items:
        pid = item.get("product_id")
        qty = item.get("quantity", 1)
        if pid not in MENU:
            return None
        p = MENU[pid]
        lt = p["price"] * qty
        subtotal += lt
        order_items.append({"product_id": pid, "name": p["name"], "quantity": qty, "line_total": lt})
    tax = round(subtotal * 0.08)
    return {"items": order_items, "subtotal": subtotal, "tax": tax, "total": subtotal + tax}

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "orders-service"}), 200

@app.route("/api/menu/")
def get_menu():
    return jsonify({"menu": MENU, "total_items": len(MENU)}), 200

@app.route("/api/orders/", methods=["POST"])
def create_order():
    data = request.get_json()
    if not data.get("customer_id") or not data.get("items"):
        return jsonify({"error": "customer_id e items son requeridos"}), 400
    totals = calculate_total(data["items"])
    if totals is None:
        return jsonify({"error": "Producto no encontrado en el menu"}), 404
    order = {
        "id": str(uuid.uuid4())[:8],
        "customer_id": data["customer_id"],
        "items": totals["items"],
        "subtotal": totals["subtotal"],
        "tax": totals["tax"],
        "total": totals["total"],
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    orders_db.append(order)
    return jsonify(order), 201

@app.route("/api/orders/<oid>/confirm", methods=["PUT"])
def confirm_order(oid):
    for o in orders_db:
        if o["id"] == oid:
            o["status"] = "confirmed"
            return jsonify({"message": "Pedido confirmado", "order": o}), 200
    return jsonify({"error": "Pedido no encontrado"}), 404

@app.route("/api/orders/<oid>")
def get_order(oid):
    for o in orders_db:
        if o["id"] == oid:
            return jsonify(o), 200
    return jsonify({"error": "Pedido no encontrado"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False)
