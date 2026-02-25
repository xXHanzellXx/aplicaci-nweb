import os
import bcrypt
import jwt
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from bson.objectid import ObjectId

# Cargar variables de entorno
load_dotenv()

# Configuración de Flask para servir archivos estáticos (HTML, CSS, JS)
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# [cite_start]Conexión a MongoDB Atlas [cite: 1]
client = MongoClient(os.getenv("MONGO_URI"))
[cite_start]db = client["vestuario"] [cite: 1]

[cite_start]users = db["users"] [cite: 1]
[cite_start]clothes = db["clothes"] [cite: 1]
[cite_start]rentals = db["rentals"] [cite: 1]
[cite_start]outfits = db["outfits"] [cite: 1]

[cite_start]JWT_SECRET = os.getenv("JWT_SECRET") [cite: 1]

# =========================
# Rutas para servir el Frontend
# =========================
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# =========================
# Middleware de Autenticación
# =========================
def token_required(func):
    def wrapper(*args, **kwargs):
        [cite_start]token = request.headers.get("Authorization") [cite: 1]
        if not token:
            [cite_start]return jsonify({"error": "Token requerido"}), 401 [cite: 1]

        try:
            # Quitamos el prefijo 'Bearer ' si existe
            if token.startswith("Bearer "):
                token = token.split(" ")[1]
            [cite_start]data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"]) [cite: 1]
            [cite_start]request.user_id = data["user_id"] [cite: 1]
        except Exception as e:
            [cite_start]return jsonify({"error": "Token inválido"}), 401 [cite: 1]

        [cite_start]return func(*args, **kwargs) [cite: 1]
    wrapper.__name__ = func.__name__
    return wrapper

# =========================
# API Endpoints
# =========================

@app.route("/api/register", methods=["POST"])
def register():
    [cite_start]data = request.json [cite: 1]
    [cite_start]if users.find_one({"email": data["email"]}): [cite: 1]
        [cite_start]return jsonify({"error": "Email ya existe"}), 400 [cite: 1]

    [cite_start]hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()) [cite: 1]
    [cite_start]users.insert_one({ [cite: 1]
        [cite_start]"name": data["name"], [cite: 1]
        [cite_start]"email": data["email"], [cite: 1]
        [cite_start]"password": hashed [cite: 1]
    })
    [cite_start]return jsonify({"message": "Usuario creado"}) [cite: 1]

@app.route("/api/login", methods=["POST"])
def login():
    [cite_start]data = request.json [cite: 1]
    [cite_start]user = users.find_one({"email": data["email"]}) [cite: 1]

    [cite_start]if not user: [cite: 1]
        [cite_start]return jsonify({"error": "Usuario no existe"}), 400 [cite: 1]

    [cite_start]if not bcrypt.checkpw(data["password"].encode(), user["password"]): [cite: 1]
        [cite_start]return jsonify({"error": "Contraseña incorrecta"}), 400 [cite: 1]

    token = jwt.encode(
        {
            [cite_start]"user_id": str(user["_id"]), [cite: 1]
            [cite_start]"exp": datetime.now(timezone.utc) + timedelta(hours=24) [cite: 1]
        },
        JWT_SECRET,
        algorithm="HS256"
    [cite_start]) [cite: 1]

    [cite_start]return jsonify({"token": token}) [cite: 1]

@app.route("/api/clothes", methods=["GET"])
def get_clothes():
    [cite_start]items = list(clothes.find()) [cite: 1]
    [cite_start]for item in items: [cite: 1]
        [cite_start]item["_id"] = str(item["_id"]) [cite: 1]
    [cite_start]return jsonify(items) [cite: 1]

@app.route("/api/rent", methods=["POST"])
@token_required
def rent():
    [cite_start]data = request.json [cite: 1]
    [cite_start]rentals.insert_one({ [cite: 1]
        [cite_start]"user_id": request.user_id, [cite: 1]
        [cite_start]"clothe_id": data["clothe_id"], [cite: 1]
        [cite_start]"date": datetime.now(timezone.utc) [cite: 1]
    })
    [cite_start]return jsonify({"message": "Alquiler realizado"}) [cite: 1]

@app.route("/api/outfit", methods=["POST"])
@token_required
def save_outfit():
    [cite_start]data = request.json [cite: 1]
    [cite_start]outfits.insert_one({ [cite: 1]
        [cite_start]"user_id": request.user_id, [cite: 1]
        [cite_start]"shirt": data["shirt"], [cite: 1]
        [cite_start]"pants": data["pants"], [cite: 1]
        [cite_start]"saved_at": datetime.now(timezone.utc) [cite: 1]
    })
    [cite_start]return jsonify({"message": "Outfit guardado"}) [cite: 1]

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
