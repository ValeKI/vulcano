from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from utils.jwt_utils import require_auth
from services.file_service import FileService
from dtos.common_dtos import ErrorResponseDTO

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
    """Carica un file per l'utente autenticato."""
    service = FileService(request)
    response_dto = service.upload_file()
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@file_bp.route("/download", methods=["GET"])
@require_auth
def download_file():
    """Scarica un file dell'utente autenticato."""
    service = FileService(request)
    response_dto = service.download_file()
    status = get_status_code(response_dto)
    if hasattr(response_dto, "file_data") and hasattr(response_dto, "file_name"):
        return send_file(
            BytesIO(response_dto.file_data),
            download_name=response_dto.file_name,
            as_attachment=True
        )
    return jsonify(response_dto.model_dump()), status

@file_bp.route("/list", methods=["GET"])
@require_auth
def list_files():
    """Restituisce la lista dei file dell'utente autenticato."""
    service = FileService(request)
    response_dto = service.list_files()
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@file_bp.route("/list_by_answer_id", methods=["GET"])
@require_auth
def list_files_by_answer_id():
    """Restituisce la lista dei file associati a una risposta."""
    service = FileService(request)
    response_dto = service.list_files_by_answer_id()
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status