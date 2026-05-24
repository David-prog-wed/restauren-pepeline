from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)
reservations_db = []
tables = [
    {"id": 1, "capacity": 2, "zone": "interior"},
    {"id": 2, "capacity": 4, "zone": "interior"},
    {"id": 3, "capacity": 4, "zone": "terraza"},
    {"id": 4, "capacity": 6, "zone": "privado"},
    {"id": 5, "capacity": 2, "zone": "terraza"},
]

def check_availability(date, time_str, party_size, ignore_cancelled=True):
    occupied = set()
    for r in reservations_db:
        if r["date"] == date and r["time"] == time_str:
            if ignore_cancelled and r["status"] == "cancelled":
                continue
            occupied.add(r["table_id"])
    available = [t for t in tables
                 if t["id"] not in occupied and t["capacity"] >= party_size]
    return {"available_tables": len(available), "tables": available}

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "reservations-service"}), 200

@app.route("/api/reservations/availability")
def availability():
    date = request.args.get("date")
    time_str = request.args.get("time")
    party_size = int(request.args.get("party_size", 2))
    if not date or not time_str:
        return jsonify({"error": "date y time son requeridos"}), 400
    return jsonify(check_availability(date, time_str, party_size)), 200

@app.route("/api/reservations/", methods=["POST"])
def create_reservation():
    data = request.get_json()
    for field in ["date", "time", "party_size", "customer_id"]:
        if field not in data:
            return jsonify({"error": f"Campo requerido: {field}"}), 400
    avail = check_availability(data["date"], data["time"], data["party_size"])
    if avail["available_tables"] == 0:
        return jsonify({"error": "Sin mesas disponibles para ese horario"}), 409
    reservation = {
        "id": str(uuid.uuid4())[:8],
        "customer_id": data["customer_id"],
        "date": data["date"],
        "time": data["time"],
        "party_size": data["party_size"],
        "table_id": avail["tables"][0]["id"],
        "status": "confirmed",
        "created_at": datetime.now().isoformat()
    }
    reservations_db.append(reservation)
    return jsonify(reservation), 201

@app.route("/api/reservations/<rid>")
def get_reservation(rid):
    for r in reservations_db:
        if r["id"] == rid:
            return jsonify(r), 200
    return jsonify({"error": "Reserva no encontrada"}), 404

@app.route("/api/reservations/<rid>/cancel", methods=["PUT"])
def cancel_reservation(rid):
    for r in reservations_db:
        if r["id"] == rid:
            r["status"] = "cancelled"
            return jsonify({"message": "Reserva cancelada", "reservation": r}), 200
    return jsonify({"error": "Reserva no encontrada"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
