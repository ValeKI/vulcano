from flask import request, jsonify
from utils.jwt_utils import decode_token

def _get_decoded_token():
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None
    if not token:
        return jsonify({"error": "Token mancante"}), 401
    decoded = decode_token(token)
    if not decoded:
        return jsonify({"error": "Token non valido"}), 401
    return decoded

def get_user_id_from_request():
    decoded = _get_decoded_token()
    if isinstance(decoded, tuple):
        return decoded
    if "id" not in decoded:
        return jsonify({"error": "Token non valido"}), 401
    return decoded["id"]

def get_username_from_request():
    decoded = _get_decoded_token()
    if isinstance(decoded, tuple):
        return decoded
    if "username" not in decoded:
        return jsonify({"error": "Token non valido"}), 401
    return decoded["username"]

def get_email_from_request():
    decoded = _get_decoded_token()
    if isinstance(decoded, tuple):
        return decoded
    if "email" not in decoded:
        return jsonify({"error": "Token non valido"}), 401
    return decoded["email"]

def get_user_from_request():
    decoded = _get_decoded_token()
    if isinstance(decoded, tuple):
        return decoded
    if not all(k in decoded for k in ("id", "username", "email")):
        return jsonify({"error": "Token non valido"}), 401
    return {
        "id": decoded["id"],
        "username": decoded["username"],
        "email": decoded["email"]
    }
