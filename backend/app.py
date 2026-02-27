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

# Configuración: Flask busca el frontend saliendo de 'backend'
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Conexión a MongoDB Atlas
client = MongoClient(os.getenv("MONGO_URI"))
db = client["vestuario"]

users = db["users"]
clothes = db["clothes"]
rentals = db["rentals"]
outfits = db["outfits"]

JWT_SECRET = os.getenv("JWT_SECRET")

# =========================
# Rutas para servir el Frontend
# =========================
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# =========================
# Middleware de Autenticación
# =========================
def token_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token requerido"}), 401
        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user_id = data["user_id"]
        except:
            return jsonify({"error": "Token inválido"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# =========================
# API Endpoints (Tu Lógica)
# =========================

# Modifica la ruta de registro en app.py
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    if users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email ya existe"}), 400
    
    # IMPORTANTE: Guardamos el hash como string para evitar líos con JSON
    hashed = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    users.insert_one({
        "name": data["name"], 
        "email": data["email"], 
        "password": hashed # MongoDB guarda esto bien
    })
    return jsonify({"message": "Usuario creado"})

# Modifica la ruta de login en app.py
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = users.find_one({"email": data["email"]})
    
    # Verificación de seguridad
    if not user or not bcrypt.checkpw(data["password"].encode('utf-8'), user["password"]):
        return jsonify({"error": "Credenciales incorrectas"}), 400
    
    token = jwt.encode({
        "user_id": str(user["_id"]),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }, JWT_SECRET, algorithm="HS256")
    
    return jsonify({"token": token})

@app.route("/api/clothes", methods=["GET"])
def get_clothes():
    items = list(clothes.find())
    for item in items: item["_id"] = str(item["_id"])
    return jsonify(items)

@app.route("/api/rent", methods=["POST"])
@token_required
def rent():
    data = request.json
    rentals.insert_one({
        "user_id": request.user_id,
        "clothe_id": data["clothe_id"],
        "date": datetime.now(timezone.utc)
    })
    return jsonify({"message": "Alquiler realizado"})

@app.route("/api/outfit", methods=["POST"])
@token_required
def save_outfit():
    data = request.json
    outfits.insert_one({
        "user_id": request.user_id,
        "shirt": data["shirt"],
        "pants": data["pants"],
        "saved_at": datetime.now(timezone.utc)
    })
    return jsonify({"message": "Outfit guardado"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

