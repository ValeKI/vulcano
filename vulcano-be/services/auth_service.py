from flask import Request, jsonify
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from db import get_cursor
from config import CURRENT_CONFIG
from utils.jwt_utils import JwtUtils
from utils.email_utils import EmailUtils
from utils.db.db_user_utils import DbUserUtils
from utils.auth_utils import AuthUtils
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
        print("[AUTH] login_service called")
        """
        Effettua il login dell'utente.
        Returns:
            dict: Token, dati utente.
            DTO: LoginResponseDTO, ErrorResponseDTO
        """
        if not cmd.usernameOrEmail or not cmd.password:
            return ErrorResponseDTO(error="Credenziali mancanti")
        db_user_utils = DbUserUtils()
        user = db_user_utils.get_user_by_username_or_email(cmd.usernameOrEmail)
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
        jwt_utils = JwtUtils()
        access_token = jwt_utils.generate_access_token(payload)
        refresh_token = jwt_utils.generate_refresh_token(payload)
        user_dto = UserDTO(username=user["username"], email=user["email"])
        print("[AUTH] login_service completed")
        return LoginResponseDTO(token=access_token, refresh_token=refresh_token, user=user_dto)

    def refresh_service(self, query: RefreshQuery):
        print("[AUTH] refresh_service called")
        """
        Rigenera il token di accesso tramite refresh token.
        Returns:
            dict: Nuovo token.
            DTO: RefreshResponseDTO, ErrorResponseDTO
        """
        refresh_token = query.refresh_token
        if not refresh_token:
            return ErrorResponseDTO(error="Nessun token di refresh")
        jwt_utils = JwtUtils()
        decoded = jwt_utils.verify_refresh_token(refresh_token)
        if not decoded:
            return ErrorResponseDTO(error="Token di refresh non valido o scaduto")
        new_access_token = jwt_utils.generate_access_token({
            "id": decoded["id"],
            "username": decoded["username"],
            "email": decoded["email"]
        })
        print("[AUTH] refresh_service completed")
        return RefreshResponseDTO(token=new_access_token)

    def check_service(self, query: CheckQuery):
        print("[AUTH] check_service called")
        """
        Verifica la validità dell'utente autenticato.
        Returns:
            dict: Stato e dati utente.
            DTO: CheckResponseDTO, ErrorResponseDTO
        """
        auth_utils = AuthUtils(self.request)
        db_user_utils = DbUserUtils()
        user = auth_utils.get_user_from_request()
        if user is None:
            return jsonify({"error": "Utente non trovato"}), 401
        db_user = db_user_utils.get_user_by_username_or_email(user["username"])
        if not db_user:
            return ErrorResponseDTO(error="Utente non trovato")
        print("[AUTH] check_service completed")
        return CheckResponseDTO(status="ok", user=user)

    def signup_service(self, cmd: SignUpCommand):
        print("[AUTH] signup_service called")
        """
        Registra un nuovo utente.
        Returns:
            dict: Stato e dati utente.
            DTO: SignUpResponseDTO, ErrorResponseDTO
        """
        db_user_utils = DbUserUtils()
        if not cmd.email or not cmd.password or not cmd.username:
            return ErrorResponseDTO(error="Dati mancanti")
        existing_user = db_user_utils.get_existing_user(cmd.email, cmd.username)
        if existing_user:
            return ErrorResponseDTO(error="Utente già esistente")
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(cmd.password.encode(), salt).decode('utf-8')
        db_user_utils.insert_user(cmd.username, cmd.email, hashed_pw)
        print("[AUTH] signup_service completed")
        return SignUpResponseDTO(status="ok", user={"username": cmd.username, "email": cmd.email})

    def forgot_password_service(self, cmd: ForgotPasswordCommand):
        print("[AUTH] forgot_password_service called")
        """
        Invia email di reset password.
        Returns:
            dict: Stato.
            DTO: ForgotPasswordResponseDTO, ErrorResponseDTO
        """
        db_user_utils = DbUserUtils()
        if not cmd.email:
            return ErrorResponseDTO(error="Email mancante")
        user = db_user_utils.get_user_by_email(cmd.email)
        if not user:
            return ForgotPasswordResponseDTO(status="ok")
        payload = {
            "id": user["id"],
            "email": user["email"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        reset_token = jwt.encode(payload, CURRENT_CONFIG.SECRET_KEY, algorithm="HS256")
        reset_link = f"{CURRENT_CONFIG.FRONTEND_BASE_URL}/reset-password?token={reset_token}"
        db_user_utils.update_user_reset_token(user["id"], reset_token)
        email_utils = EmailUtils()
        email_utils.send_reset_email(cmd.email, reset_link)
        print("[AUTH] forgot_password_service completed")
        return ForgotPasswordResponseDTO(status="ok")

    def reset_password_service(self, cmd: ResetPasswordCommand):
        print("[AUTH] reset_password_service called")
        """
        Aggiorna la password dell'utente tramite token di reset.
        Returns:
            dict: Stato.
            DTO: ResetPasswordResponseDTO, ErrorResponseDTO
        """
        db_user_utils = DbUserUtils()
        if not cmd.token or not cmd.new_password:
            return ErrorResponseDTO(error="Token o nuova password mancanti")
        jwt_utils = JwtUtils()
        try:
            decoded = jwt_utils.decode_token(cmd.token)
            user_id = decoded["id"]
        except jwt.ExpiredSignatureError:
            return ErrorResponseDTO(error="Token scaduto")
        except jwt.InvalidTokenError:
            return ErrorResponseDTO(error="Token non valido")
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(cmd.new_password.encode(), salt).decode('utf-8')
        rowcount = db_user_utils.update_user_password_and_reset_token(user_id, hashed_pw, cmd.token)
        if rowcount == 0:
            return ErrorResponseDTO(error="Token non valido")
        print("[AUTH] reset_password_service completed")
        return ResetPasswordResponseDTO(status="ok")
