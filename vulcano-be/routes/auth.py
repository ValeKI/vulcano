from flask import Blueprint, request, jsonify, make_response
import jwt
from db import get_cursor
from utils.jwt_utils import generate_refresh_token, generate_access_token, verify_token, verify_refresh_token
import bcrypt
from utils.email_utils import send_reset_email
from datetime import datetime, timedelta, timezone
from config import CURRENT_CONFIG

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
    if not user:
        return jsonify({"error": "Credenziali non valide"}), 401

    db_password = user["password"]
    if isinstance(db_password, str):
        db_password = db_password.encode()

    try:
        if not bcrypt.checkpw(password.encode(), db_password):
            return jsonify({"error": "Credenziali non valide"}), 401
    except ValueError:
        return jsonify({"error": "Password non valida nel database"}), 400

    payload = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"]
    }

    access_token = generate_access_token(payload)
    refresh_token = generate_refresh_token(payload)

    response = make_response(jsonify({
        "token": access_token,
        "user": {"username": user["username"], "email": user["email"]}
    }))

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=60 * 60 * 24 * 7  # 7 giorni
    )

    return response


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        return jsonify({"error": "Nessun token di refresh"}), 401

    decoded = verify_refresh_token(refresh_token)
    if not decoded:
        return jsonify({"error": "Token di refresh non valido o scaduto"}), 401

    new_access_token = generate_access_token({
        "id": decoded["id"],
        "username": decoded["username"],
        "email": decoded["email"]
    })

    return jsonify({"token": new_access_token})

@auth_bp.route("/check", methods=["POST"])
def check():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token mancante"}), 401

    token = auth_header.split(" ")[1]  # rimuove 'Bearer '
    decoded = verify_token(token)

    if not decoded:
        return jsonify({"error": "Token non valido o scaduto"}), 401

    return jsonify({
        "status": "ok",
        "user": {
            "id": decoded["id"],
            "username": decoded["username"],
            "email": decoded["email"]
        }
    })

@auth_bp.route("/signUp", methods=["POST"])
def signUp():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")

    if not email or not password or not username:
        return jsonify({"error": "Dati mancanti"}), 400

    cur = get_cursor()
    cur.execute("SELECT * FROM users WHERE email=%s OR username=%s", (email, username))
    existing_user = cur.fetchone()

    if existing_user:
        return jsonify({"error": "Utente già esistente"}), 409
    
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode(), salt).decode('utf-8')

    cur.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed_pw)
    )
    cur.connection.commit()

    return jsonify({"status": "ok", "user": {"username": username, "email": email}})

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email mancante"}), 400

    cur = get_cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    if not user:
        return jsonify({"status": "ok"}), 200

    payload = {
        "id": user["id"],
        "email": user["email"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    import jwt
    from config import CURRENT_CONFIG
    reset_token = jwt.encode(payload, CURRENT_CONFIG.SECRET_KEY, algorithm="HS256")
    reset_link = f"{CURRENT_CONFIG.FRONTEND_BASE_URL}/reset-password?token={reset_token}"
    send_reset_email(email, reset_link)
    return jsonify({"status": "ok"}), 200

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    token = data.get("token")
    new_password = data.get("new_password")
    if not token or not new_password:
        return jsonify({"error": "Token o nuova password mancanti"}), 400

    try:
        decoded = jwt.decode(token, CURRENT_CONFIG.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["id"]
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token scaduto"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token non valido"}), 400
    
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(new_password.encode(), salt).decode('utf-8')

    cur = get_cursor()
    result = cur.execute(
        "UPDATE users SET password=%s, reset_token=NULL WHERE id=%s AND reset_token=%s",
        (hashed_pw, user_id, token)
    )
    if cur.rowcount == 0:
        return jsonify({"error": "Token non valido"}), 400

    cur.connection.commit()
    return jsonify({"status": "ok"}), 200