from flask import Blueprint, request, jsonify, make_response
from utils.jwt_utils import require_auth
from services.auth_service import AuthService

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
    """Effettua il login dell'utente.

    ---
    post:
      summary: Effettua il login dell'utente.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                usernameOrEmail:
                  type: string
                password:
                  type: string
      responses:
        200:
          description: Login effettuato con successo.
        400:
          description: Credenziali mancanti.
        401:
          description: Credenziali non valide.
    """
    service = AuthService(request)
    result = service.login_service()
    status = get_status_code(result)
    if "refresh_token" in result:
        response = make_response(jsonify({
            "token": result["token"],
            "user": result["user"]
        }), status)
        response.set_cookie(
            "refresh_token",
            result["refresh_token"],
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=60 * 60 * 24 * 7
        )
        return response
    return jsonify(result), status

@auth_bp.route("/refresh", methods=["POST"])
@require_auth
def refresh():
    """Rigenera il token di accesso tramite refresh token.

    ---
    post:
      summary: Rigenera il token di accesso tramite refresh token.
      responses:
        200:
          description: Token rigenerato con successo.
        401:
          description: Token di refresh non valido o mancante.
    """
    service = AuthService(request)
    result = service.refresh_service()
    status = get_status_code(result)
    return jsonify(result), status

@auth_bp.route("/check", methods=["POST"])
@require_auth
def check():
    """Verifica la validità dell'utente autenticato.

    ---
    post:
      summary: Verifica la validità dell'utente autenticato.
      responses:
        200:
          description: Utente valido.
        404:
          description: Utente non trovato.
    """
    service = AuthService(request)
    result = service.check_service()
    status = get_status_code(result)
    return jsonify(result), status

@auth_bp.route("/signUp", methods=["POST"])
def signUp():
    """Registra un nuovo utente.

    ---
    post:
      summary: Registra un nuovo utente.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                email:
                  type: string
                password:
                  type: string
      responses:
        200:
          description: Registrazione effettuata con successo.
        400:
          description: Dati mancanti.
        409:
          description: Utente già esistente.
    """
    service = AuthService(request)
    result = service.signup_service()
    status = get_status_code(result)
    return jsonify(result), status

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    """Invia email di reset password.

    ---
    post:
      summary: Invia email di reset password.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
      responses:
        200:
          description: Email inviata o utente non trovato.
        400:
          description: Email mancante.
    """
    service = AuthService(request)
    result = service.forgot_password_service()
    status = get_status_code(result)
    return jsonify(result), status

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """Aggiorna la password dell'utente tramite token di reset.

    ---
    post:
      summary: Aggiorna la password dell'utente tramite token di reset.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                token:
                  type: string
                new_password:
                  type: string
      responses:
        200:
          description: Password aggiornata con successo.
        400:
          description: Token o nuova password mancanti, token scaduto o non valido.
    """
    service = AuthService(request)
    result = service.reset_password_service()
    status = get_status_code(result)
    return jsonify(result), status