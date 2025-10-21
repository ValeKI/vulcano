import jwt
from datetime import datetime, timedelta, timezone
from config import CURRENT_CONFIG
from functools import wraps
from flask import request, jsonify
from utils.db.db_user_utils import DbUserUtils

class JwtUtils:
    SECRET_KEY = CURRENT_CONFIG.SECRET_KEY
    REFRESH_SECRET_KEY = CURRENT_CONFIG.REFRESH_SECRET_KEY

    def generate_access_token(self, payload: dict, expires_in: int = 86400):
        print(f"[JWT] Generating access token for payload: {payload}")
        payload_copy = payload.copy()
        payload_copy["exp"] = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        token = jwt.encode(payload_copy, self.SECRET_KEY, algorithm="HS256")
        print(f"[JWT] Access token generated")
        return token

    def generate_refresh_token(self, payload: dict, expires_in: int = 60 * 60 * 24 * 7):  # 7 giorni
        print(f"[JWT] Generating refresh token for payload: {payload}")
        data = payload.copy()
        data["exp"] = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        x = jwt.encode(data, self.REFRESH_SECRET_KEY, algorithm="HS256")
        print(f"[JWT] Refresh token generated")
        return x

    def verify_token(self, token: str):
        print(f"[JWT] Verifying access token: {token}")
        try:
            decoded = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            print(f"[JWT] Token verification result: {decoded if decoded else 'Invalid/Expired'}")
            return decoded if 'decoded' in locals() else None
        except jwt.ExpiredSignatureError as e:
            return None
        except jwt.InvalidTokenError as e:
            return None

    def verify_refresh_token(self, token: str):
        print(f"[JWT] Verifying refresh token: {token}")
        try:
            decoded = jwt.decode(token, self.REFRESH_SECRET_KEY, algorithms=["HS256"])
            print(f"[JWT] Refresh token verification result: {decoded if decoded else 'Invalid/Expired'}")
            return decoded if 'decoded' in locals() else None
        except jwt.ExpiredSignatureError as e:
            return None
        except jwt.InvalidTokenError as e:
            return None

    def decode_token(self, token: str):
        print(f"[JWT] Decoding token: {token}")
        decoded = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
        print(f"[JWT] Decoded token: {decoded}")
        return decoded

# Funzione esterna per la verifica del token e dell'utente
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("[JWT] require_auth called")
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
        db_user_utils = DbUserUtils()
        user = db_user_utils.get_user_by_username_or_email(username)
        if not user:
            return jsonify({"error": "Utente non trovato"}), 401
        print("[JWT] User authenticated")
        return f(*args, **kwargs)
    return decorated