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
from dtos.common_dtos import ErrorResponseDTO
from dtos.auth_dtos import UserDTO, LoginResponseDTO, RefreshResponseDTO, CheckResponseDTO, SignUpResponseDTO, ForgotPasswordResponseDTO, ResetPasswordResponseDTO
from commands.auth_commands import LoginCommand, SignUpCommand, ForgotPasswordCommand, ResetPasswordCommand
from queries.auth_queries import RefreshQuery, CheckQuery

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

    def login_service(self, cmd: LoginCommand):
        """
        Effettua il login dell'utente.
        Returns:
            dict: Token, dati utente.
            DTO: LoginResponseDTO, ErrorResponseDTO
        """
        if not cmd.usernameOrEmail or not cmd.password:
            return ErrorResponseDTO(error="Credenziali mancanti")
        user = get_user_by_username_or_email(cmd.usernameOrEmail)
        if not user:
            return ErrorResponseDTO(error="Credenziali non valide")
        db_password = user["password"]
        if isinstance(db_password, str):
            db_password = db_password.encode()
        try:
            if not bcrypt.checkpw(cmd.password.encode(), db_password):
                return ErrorResponseDTO(error="Credenziali non valide")
        except ValueError:
            return ErrorResponseDTO(error="Password non valida nel database")
        payload = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
        access_token = generate_access_token(payload)
        refresh_token = generate_refresh_token(payload)
        user_dto = UserDTO(username=user["username"], email=user["email"])
        return LoginResponseDTO(token=access_token, refresh_token=refresh_token, user=user_dto)

    def refresh_service(self, query: RefreshQuery):
        """
        Rigenera il token di accesso tramite refresh token.
        Returns:
            dict: Nuovo token.
            DTO: RefreshResponseDTO, ErrorResponseDTO
        """
        refresh_token = query.refresh_token
        if not refresh_token:
            return ErrorResponseDTO(error="Nessun token di refresh")
        decoded = verify_refresh_token(refresh_token)
        if not decoded:
            return ErrorResponseDTO(error="Token di refresh non valido o scaduto")
        new_access_token = generate_access_token({
            "id": decoded["id"],
            "username": decoded["username"],
            "email": decoded["email"]
        })
        return RefreshResponseDTO(token=new_access_token)

    def check_service(self, query: CheckQuery):
        """
        Verifica la validità dell'utente autenticato.
        Returns:
            dict: Stato e dati utente.
            DTO: CheckResponseDTO, ErrorResponseDTO
        """
        user = get_user_from_request()
        if isinstance(user, tuple):  # Se è una response di errore
            return ErrorResponseDTO(error="Utente non trovato")
        db_user = get_user_by_username_or_email(user["username"])
        if not db_user:
            return ErrorResponseDTO(error="Utente non trovato")
        return CheckResponseDTO(status="ok", user=user)

    def signup_service(self, cmd: SignUpCommand):
        """
        Registra un nuovo utente.
        Returns:
            dict: Stato e dati utente.
            DTO: SignUpResponseDTO, ErrorResponseDTO
        """
        if not cmd.email or not cmd.password or not cmd.username:
            return ErrorResponseDTO(error="Dati mancanti")
        existing_user = get_existing_user(cmd.email, cmd.username)
        if existing_user:
            return ErrorResponseDTO(error="Utente già esistente")
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(cmd.password.encode(), salt).decode('utf-8')
        insert_user(cmd.username, cmd.email, hashed_pw)
        return SignUpResponseDTO(status="ok", user={"username": cmd.username, "email": cmd.email})

    def forgot_password_service(self, cmd: ForgotPasswordCommand):
        """
        Invia email di reset password.
        Returns:
            dict: Stato.
            DTO: ForgotPasswordResponseDTO, ErrorResponseDTO
        """
        if not cmd.email:
            return ErrorResponseDTO(error="Email mancante")
        user = get_user_by_email(cmd.email)
        if not user:
            return ForgotPasswordResponseDTO(status="ok")
        payload = {
            "id": user["id"],
            "email": user["email"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        reset_token = jwt.encode(payload, CURRENT_CONFIG.SECRET_KEY, algorithm="HS256")
        reset_link = f"{CURRENT_CONFIG.FRONTEND_BASE_URL}/reset-password?token={reset_token}"
        update_user_reset_token(user["id"], reset_token)
        send_reset_email(cmd.email, reset_link)
        return ForgotPasswordResponseDTO(status="ok")

    def reset_password_service(self, cmd: ResetPasswordCommand):
        """
        Aggiorna la password dell'utente tramite token di reset.
        Returns:
            dict: Stato.
            DTO: ResetPasswordResponseDTO, ErrorResponseDTO
        """
        if not cmd.token or not cmd.new_password:
            return ErrorResponseDTO(error="Token o nuova password mancanti")
        try:
            decoded = jwt.decode(cmd.token, CURRENT_CONFIG.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded["id"]
        except jwt.ExpiredSignatureError:
            return ErrorResponseDTO(error="Token scaduto")
        except jwt.InvalidTokenError:
            return ErrorResponseDTO(error="Token non valido")
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(cmd.new_password.encode(), salt).decode('utf-8')
        rowcount = update_user_password_and_reset_token(user_id, hashed_pw, cmd.token)
        if rowcount == 0:
            return ErrorResponseDTO(error="Token non valido")
        return ResetPasswordResponseDTO(status="ok")
