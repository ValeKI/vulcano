from flask import Blueprint, request, jsonify, send_file
import os
from io import BytesIO
from utils.jwt_utils import require_auth
from utils.file_utils import get_unique_file_name, insert_new_file
from utils.minio_utils import upload_user_file, get_user_file
from utils.auth_utils import get_user_id_from_request
from utils.db.db_file_utils import list_files_for_user, get_file_by_id
from utils.qdrant_utils import upload_file_chunks_to_qdrant, get_file_ids_by_user_id, get_file_ids_by_answer_id

file_bp = Blueprint("files", __name__)

@file_bp.route("/upload", methods=["POST"])
@require_auth
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Nessun file inviato"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nome file mancante"}), 400

    user_id = get_user_id_from_request()
    if isinstance(user_id, tuple):
        return user_id

    print("user_id:", user_id)
    new_file_name = get_unique_file_name(file.filename, user_id)

    file_content = file.read()
    if not file_content:
        return jsonify({"error": "File vuoto"}), 400

    upload_user_file(user_id, new_file_name, file_content)
    file_id = insert_new_file(new_file_name, user_id)

    num_chunks = upload_file_chunks_to_qdrant(user_id, file_id, new_file_name, file_content)
    if num_chunks == 0:
        return jsonify({"error": "File vuoto o non processabile"}), 400

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

    file_ids = get_file_ids_by_user_id(user_id)
    files = []
    for file_id in file_ids:
        file_data = get_file_by_id(file_id)
        if file_data:
            files.append(file_data)
    return jsonify({"files": files})

@file_bp.route("/list_by_answer_id", methods=["GET"])
@require_auth
def list_files_by_answer_id():
    answer_id = request.args.get("answer_id")
    if not answer_id:
        return jsonify({"error": "answer_id mancante"}), 400

    try:
        answer_id = int(answer_id)
    except Exception:
        return jsonify({"error": "answer_id non valido"}), 400

    file_ids = get_file_ids_by_answer_id(answer_id)
    files = []
    for file_id in file_ids:
        file_data = get_file_by_id(file_id)
        if file_data:
            files.append(file_data)
    return jsonify({"files": files})