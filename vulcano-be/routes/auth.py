from flask import Blueprint, request, jsonify, make_response
from utils.jwt_utils import require_auth
from services.auth_service import AuthService
from dtos.common_dtos import ErrorResponseDTO
from dtos.auth_dtos import UserDTO, LoginResponseDTO, RefreshResponseDTO, CheckResponseDTO, SignUpResponseDTO, ForgotPasswordResponseDTO, ResetPasswordResponseDTO
from commands.auth_commands import LoginCommand, SignUpCommand, ForgotPasswordCommand, ResetPasswordCommand
from queries.auth_queries import RefreshQuery, CheckQuery

auth_bp = Blueprint("auth", __name__)

def get_status_code(result, default=200):
    if not isinstance(result, dict):
        return default
    if "error" in result:
        error_map = {
            "Credenziali mancanti": 400,
            "Credenziali non valide": 401,
            "Password non valida nel database": 400,
            "Nessun token di refresh": 401,
            "Token di refresh non valido o scaduto": 401,
            "Utente non trovato": 404,
            "Dati mancanti": 400,
            "Utente già esistente": 409,
            "Email mancante": 400,
            "Token o nuova password mancanti": 400,
            "Token scaduto": 400,
            "Token non valido": 400,
        }
        return error_map.get(result["error"], 400)
    return default

@auth_bp.route("/login", methods=["POST"])
def login():
    print("[ROUTE] /login called")
    """Effettua il login dell'utente."""
    cmd = LoginCommand(**request.get_json())
    service = AuthService(request)
    response_dto = service.login_service(cmd)
    status = get_status_code(response_dto)
    if hasattr(response_dto, "refresh_token"):
        response = make_response(jsonify(response_dto.model_dump()), status)
        response.set_cookie(
            "refresh_token",
            response_dto.refresh_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=60 * 60 * 24 * 7
        )
        return response
    return jsonify(response_dto.model_dump()), status

@auth_bp.route("/refresh", methods=["POST"])
@require_auth
def refresh():
    print("[ROUTE] /refresh called")
    """Rigenera il token di accesso tramite refresh token."""
    query = RefreshQuery(refresh_token=request.cookies.get("refresh_token"))
    service = AuthService(request)
    response_dto = service.refresh_service(query)
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@auth_bp.route("/check", methods=["POST"])
@require_auth
def check():
    print("[ROUTE] /check called")
    """Verifica la validità dell'utente autenticato."""
    query = CheckQuery()
    service = AuthService(request)
    response_dto = service.check_service(query)
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@auth_bp.route("/signUp", methods=["POST"])
def signUp():
    print("[ROUTE] /signUp called")
    """Registra un nuovo utente."""
    cmd = SignUpCommand(**request.get_json())
    service = AuthService(request)
    response_dto = service.signup_service(cmd)
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    print("[ROUTE] /forgot-password called")
    """Invia email di reset password."""
    cmd = ForgotPasswordCommand(**request.get_json())
    service = AuthService(request)
    response_dto = service.forgot_password_service(cmd)
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    print("[ROUTE] /reset-password called")
    """Aggiorna la password dell'utente tramite token di reset."""
    cmd = ResetPasswordCommand(**request.get_json())
    service = AuthService(request)
    response_dto = service.reset_password_service(cmd)
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status