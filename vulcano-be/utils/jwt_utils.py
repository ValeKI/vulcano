import jwt
from datetime import datetime, timedelta, timezone
from config import CURRENT_CONFIG
from functools import wraps
from flask import request, jsonify
from utils.db.db_user_utils import get_user_by_username_or_email

class JwtUtils:
    SECRET_KEY = CURRENT_CONFIG.SECRET_KEY
    REFRESH_SECRET_KEY = CURRENT_CONFIG.REFRESH_SECRET_KEY

    def generate_access_token(self, payload: dict, expires_in: int = 86400):
        payload_copy = payload.copy()
        payload_copy["exp"] = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        token = jwt.encode(payload_copy, self.SECRET_KEY, algorithm="HS256")
        return token

    def generate_refresh_token(self, payload: dict, expires_in: int = 60 * 60 * 24 * 7):  # 7 giorni
        print("Generated refresh token in utils - input payload:", payload)
        data = payload.copy()
        data["exp"] = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        x = jwt.encode(data, self.REFRESH_SECRET_KEY, algorithm="HS256")
        print("Generated refresh token in util:", x)
        return x

    def verify_token(self, token: str):
        try:
            decoded = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            return decoded
        except jwt.ExpiredSignatureError as e:
            return None
        except jwt.InvalidTokenError as e:
            return None

    def verify_refresh_token(self, token: str):
        try:
            decoded = jwt.decode(token, self.REFRESH_SECRET_KEY, algorithms=["HS256"])
            return decoded
        except jwt.ExpiredSignatureError as e:
            return None
        except jwt.InvalidTokenError as e:
            return None

    def decode_token(self, token: str):
        return jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])

# Funzione esterna per la verifica del token e dell'utente
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token mancante"}), 401
        token = auth_header.split(" ")[1]
        jwt_utils = JwtUtils()
        decoded = jwt_utils.verify_token(token)
        if not decoded:
            return jsonify({"error": "Token non valido"}), 401
        username = decoded.get("username")
        if not username:
            return jsonify({"error": "Token non valido"}), 401
        user = get_user_by_username_or_email(username)
        if not user:
            return jsonify({"error": "Utente non trovato"}), 401
        # Passa l'utente autenticato alla rotta come keyword argument
        return f(*args, **kwargs)
    return decorated