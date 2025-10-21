from flask import Request
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from db import get_cursor
from config import CURRENT_CONFIG
from utils.jwt_utils import generate_refresh_token, generate_access_token, require_auth, verify_token, verify_refresh_token
from utils.email_utils import send_reset_email
from utils.db.db_user_utils import (
    get_user_by_username_or_email,
    get_user_by_email,
    get_existing_user,
    insert_user,
    update_user_password_and_reset_token,
    update_user_reset_token,
    get_user_reset_token
)
from utils.auth_utils import get_user_from_request

class AuthService:
    """
    Service per la gestione dell'autenticazione utente: login, refresh, registrazione, password reset.
    """

    def __init__(self, request: Request):
        """
        Inizializza il service con la richiesta Flask.
        Args:
            request (Request): Oggetto request Flask.
        """
        self.request = request

    def login_service(self):
        """
        Effettua il login dell'utente.
        Returns:
            dict: Token, dati utente.
        """
        data = self.request.get_json()
        usernameOrEmail = data.get("usernameOrEmail")
        password = data.get("password")

        if not usernameOrEmail or not password:
            return {"error": "Credenziali mancanti"}

        user = get_user_by_username_or_email(usernameOrEmail)
        if not user:
            return {"error": "Credenziali non valide"}

        db_password = user["password"]
        if isinstance(db_password, str):
            db_password = db_password.encode()

        try:
            if not bcrypt.checkpw(password.encode(), db_password):
                return {"error": "Credenziali non valide"}
        except ValueError:
            return {"error": "Password non valida nel database"}

        payload = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }

        access_token = generate_access_token(payload)
        refresh_token = generate_refresh_token(payload)

        return {
            "token": access_token,
            "refresh_token": refresh_token,
            "user": {"username": user["username"], "email": user["email"]}
        }

    def refresh_service(self):
        """
        Rigenera il token di accesso tramite refresh token.
        Returns:
            dict: Nuovo token.
        """
        refresh_token = self.request.cookies.get("refresh_token")
        if not refresh_token:
            return {"error": "Nessun token di refresh"}

        decoded = verify_refresh_token(refresh_token)
        if not decoded:
            return {"error": "Token di refresh non valido o scaduto"}

        new_access_token = generate_access_token({
            "id": decoded["id"],
            "username": decoded["username"],
            "email": decoded["email"]
        })

        return {"token": new_access_token}

    def check_service(self):
        """
        Verifica la validità dell'utente autenticato.
        Returns:
            dict: Stato e dati utente.
        """
        user = get_user_from_request()
        if isinstance(user, tuple):  # Se è una response di errore
            return user

        db_user = get_user_by_username_or_email(user["username"])
        if not db_user:
            return {"error": "Utente non trovato"}

        return {
            "status": "ok",
            "user": user
        }

    def signup_service(self):
        """
        Registra un nuovo utente.
        Returns:
            dict: Stato e dati utente.
        """
        data = self.request.get_json()
        email = data.get("email")
        password = data.get("password")
        username = data.get("username")

        if not email or not password or not username:
            return {"error": "Dati mancanti"}

        existing_user = get_existing_user(email, username)
        if existing_user:
            return {"error": "Utente già esistente"}

        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode(), salt).decode('utf-8')

        insert_user(username, email, hashed_pw)

        return {"status": "ok", "user": {"username": username, "email": email}}

    def forgot_password_service(self):
        """
        Invia email di reset password.
        Returns:
            dict: Stato.
        """
        data = self.request.get_json()
        email = data.get("email")
        if not email:
            return {"error": "Email mancante"}

        user = get_user_by_email(email)
        if not user:
            return {"status": "ok"}

        payload = {
            "id": user["id"],
            "email": user["email"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        reset_token = jwt.encode(payload, CURRENT_CONFIG.SECRET_KEY, algorithm="HS256")
        reset_link = f"{CURRENT_CONFIG.FRONTEND_BASE_URL}/reset-password?token={reset_token}"
        update_user_reset_token(user["id"], reset_token)
        send_reset_email(email, reset_link)
        return {"status": "ok"}

    def reset_password_service(self):
        """
        Aggiorna la password dell'utente tramite token di reset.
        Returns:
            dict: Stato.
        """
        data = self.request.get_json()
        token = data.get("token")
        new_password = data.get("new_password")
        if not token or not new_password:
            return {"error": "Token o nuova password mancanti"}

        try:
            decoded = jwt.decode(token, CURRENT_CONFIG.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded["id"]
        except jwt.ExpiredSignatureError:
            return {"error": "Token scaduto"}
        except jwt.InvalidTokenError:
            return {"error": "Token non valido"}

        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(new_password.encode(), salt).decode('utf-8')

        rowcount = update_user_password_and_reset_token(user_id, hashed_pw, token)
        if rowcount == 0:
            return {"error": "Token non valido"}

        return {"status": "ok"}
