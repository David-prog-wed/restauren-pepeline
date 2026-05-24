from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime, os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
SECRET_KEY = os.getenv("SECRET_KEY", "restaurant-secret-dev-key-2026")
users_db = {}

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "auth-service"}), 200

@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    if not email or not password or not name:
        return jsonify({"error": "Todos los campos son requeridos"}), 400
    if email in users_db:
        return jsonify({"error": "El usuario ya existe"}), 409
    users_db[email] = {
        "name": name,
        "password": generate_password_hash(password),
        "role": "customer"
    }
    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = users_db.get(email)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Credenciales invalidas"}), 401
    token = jwt.encode(
        {"email": email, "role": user["role"],
         "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)},
        SECRET_KEY, algorithm="HS256"
    )
    return jsonify({"token": token, "name": user["name"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
