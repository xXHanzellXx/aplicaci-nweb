import os
import bcrypt
import jwt
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["vestuario"]

users = db["users"]
clothes = db["clothes"]
rentals = db["rentals"]
outfits = db["outfits"]

JWT_SECRET = os.getenv("JWT_SECRET")

# =========================
# Middleware simple
# =========================
def token_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token requerido"}), 401

        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user_id = data["user_id"]
        except:
            return jsonify({"error": "Token inválido"}), 401

        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# =========================
# Registro
# =========================
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json

    if users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email ya existe"}), 400

    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    users.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": hashed
    })

    return jsonify({"message": "Usuario creado"})

# =========================
# Login
# =========================
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = users.find_one({"email": data["email"]})

    if not user:
        return jsonify({"error": "Usuario no existe"}), 400

    if not bcrypt.checkpw(data["password"].encode(), user["password"]):
        return jsonify({"error": "Contraseña incorrecta"}), 400

    token = jwt.encode(
        {
            "user_id": str(user["_id"]),
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        JWT_SECRET,
        algorithm="HS256"
    )

    return jsonify({"token": token})

# =========================
# Obtener catálogo
# =========================
@app.route("/api/clothes", methods=["GET"])
def get_clothes():
    items = list(clothes.find())
    for item in items:
        item["_id"] = str(item["_id"])
    return jsonify(items)

# =========================
# Crear alquiler
# =========================
@app.route("/api/rent", methods=["POST"])
@token_required
def rent():
    data = request.json

    rentals.insert_one({
        "user_id": request.user_id,
        "clothe_id": data["clothe_id"],
        "date": datetime.utcnow()
    })

    return jsonify({"message": "Alquiler realizado"})

# =========================
# Guardar outfit
# =========================
@app.route("/api/outfit", methods=["POST"])
@token_required
def save_outfit():
    data = request.json

    outfits.insert_one({
        "user_id": request.user_id,
        "shirt": data["shirt"],
        "pants": data["pants"],
        "saved_at": datetime.utcnow()
    })

    return jsonify({"message": "Outfit guardado"})
    
if __name__ == "__main__":
    app.run(debug=True)