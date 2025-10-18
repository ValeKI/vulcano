from flask import Blueprint, request, jsonify
from db import get_cursor
from utils.jwt_utils import generate_token, decode_token
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    usernameOrEmail = data.get("usernameOrEmail")
    password = data.get("password")

    if not usernameOrEmail or not password:
        return jsonify({"error": "Credenziali mancanti"}), 400

    cur = get_cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=%s OR email=%s",
        (usernameOrEmail, usernameOrEmail)
    )
    user = cur.fetchone()

    # TODO password hashing
    # if not user or not bcrypt.checkpw(password.encode(), user["password"].encode()):
    if not user or password != user["password"]:
        return jsonify({"error": "Credenziali non valide"}), 401

    token = generate_token({"id": user["id"], "username": user["username"], "email": user["email"]})
    return jsonify({"token": token, "user": {"username": user["username"], "email": user["email"]}})

@auth_bp.route("/check", methods=["POST"])
def check():
    # Mock: ritorna sempre "ok" e un utente finto
    return jsonify({
        "status": "ok",
        "user": {
            "username": "mockuser",
            "email": "mockuser@example.com"
        }
    })