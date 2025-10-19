from flask import Blueprint, request, jsonify, send_file
import os
from io import BytesIO
from utils.jwt_utils import require_auth
from utils.file_utils import get_unique_file_name, insert_file_with_unique_name
from utils.minio_utils import upload_user_file, get_user_file
from utils.auth_utils import get_user_id_from_request
from utils.db.db_file_utils import list_files_for_user

file_bp = Blueprint("file", __name__)

@file_bp.route("/upload", methods=["POST"])
@require_auth
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Nessun file inviato"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nome file mancante"}), 400

    # Estrai user_id dal token usando auth_utils
    user_id = get_user_id_from_request()
    if isinstance(user_id, tuple):
        return user_id

    # Ottieni nome unico
    new_file_name = get_unique_file_name(file.filename, user_id)

    # Carica su MinIO
    upload_user_file(user_id, new_file_name, file.read())

    insert_file_with_unique_name(new_file_name, user_id)

    return jsonify({"status": "ok", "filename": new_file_name})

@file_bp.route("/download", methods=["GET"])
@require_auth
def download_file():
    filename = request.args.get("filename")
    if not filename:
        return jsonify({"error": "Nome file mancante"}), 400

    user_id = get_user_id_from_request()
    if isinstance(user_id, tuple):
        return user_id

    try:
        file_data = get_user_file(user_id, filename)
    except Exception:
        return jsonify({"error": "File non trovato"}), 404

    return send_file(
        BytesIO(file_data),
        download_name=filename,
        as_attachment=True
    )

@file_bp.route("/list", methods=["GET"])
@require_auth
def list_files():
    user_id = get_user_id_from_request()
    if isinstance(user_id, tuple):
        return user_id

    files = list_files_for_user(user_id)
    return jsonify({"files": files})