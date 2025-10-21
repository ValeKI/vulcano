from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from utils.jwt_utils import require_auth
from services.file_service import FileService

file_bp = Blueprint("files", __name__)

def get_status_code(result, default=200):
    if not isinstance(result, dict):
        return default
    if "error" in result:
        error_map = {
            "Nessun file inviato": 400,
            "Nome file mancante": 400,
            "File vuoto": 400,
            "File vuoto o non processabile": 400,
            "ID file mancante": 400,
            "File non trovato": 404,
            "answer_id mancante": 400,
            "answer_id non valido": 400,
        }
        return error_map.get(result["error"], 400)
    return default

@file_bp.route("/upload", methods=["POST"])
@require_auth
def upload_file():
    """Carica un file per l'utente autenticato.

    ---
    post:
      summary: Carica un file per l'utente autenticato.
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
      responses:
        200:
          description: File caricato con successo.
        400:
          description: Errore nell'upload del file.
    """
    service = FileService(request)
    result = service.upload_file()
    status = get_status_code(result)
    return jsonify(result), status

@file_bp.route("/download", methods=["GET"])
@require_auth
def download_file():
    """Scarica un file dell'utente autenticato.

    ---
    get:
      summary: Scarica un file dell'utente autenticato.
      parameters:
        - in: query
          name: file_id
          schema:
            type: string
          required: true
      responses:
        200:
          description: File scaricato con successo.
        400:
          description: ID file mancante.
        404:
          description: File non trovato.
    """
    service = FileService(request)
    result = service.download_file()
    status = get_status_code(result)
    if "file_data" in result and "file_name" in result:
        return send_file(
            BytesIO(result["file_data"]),
            download_name=result["file_name"],
            as_attachment=True
        )
    return jsonify(result), status

@file_bp.route("/list", methods=["GET"])
@require_auth
def list_files():
    """Restituisce la lista dei file dell'utente autenticato.

    ---
    get:
      summary: Restituisce la lista dei file dell'utente autenticato.
      responses:
        200:
          description: Lista file restituita con successo.
    """
    service = FileService(request)
    result = service.list_files()
    status = get_status_code(result)
    return jsonify(result), status

@file_bp.route("/list_by_answer_id", methods=["GET"])
@require_auth
def list_files_by_answer_id():
    """Restituisce la lista dei file associati a una risposta.

    ---
    get:
      summary: Restituisce la lista dei file associati a una risposta.
      parameters:
        - in: query
          name: answer_id
          schema:
            type: string
          required: true
      responses:
        200:
          description: Lista file restituita con successo.
        400:
          description: answer_id mancante o non valido.
    """
    service = FileService(request)
    result = service.list_files_by_answer_id()
    status = get_status_code(result)
    return jsonify(result), status