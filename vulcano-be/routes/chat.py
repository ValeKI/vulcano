from flask import Blueprint, request, jsonify
from services.chat_service import ChatService
from utils.auth_utils import AuthUtils
from utils.jwt_utils import require_auth
from dtos.common_dtos import ErrorResponseDTO

chat_bp = Blueprint('chat', __name__)

def get_status_code(result, default=200):
    if not isinstance(result, dict):
        return default
    if "error" in result:
        error_map = {
            "Question not found": 404,
            "Nessun file disponibile per l'utente": 400,
            "Answer not found": 404,
        }
        return error_map.get(result["error"], 400)
    return default

@chat_bp.route('/questions/<int:question_id>', methods=['GET'])
@require_auth
def api_get_question_by_id(question_id):
    """Restituisce una domanda tramite ID."""
    service = ChatService(request)
    response_dto = service.get_question_by_id(question_id)
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@chat_bp.route('/questions/user', methods=['GET'])
@require_auth
def api_list_questions_by_user_id():
    """Restituisce la lista delle domande dell'utente autenticato."""
    service = ChatService(request)
    response_dto = service.list_questions_by_user_id()
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@chat_bp.route('/questions', methods=['POST'])
@require_auth
def api_insert_question():
    """Inserisce una nuova domanda e genera la risposta."""
    service = ChatService(request)
    response_dto = service.insert_question()
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@chat_bp.route('/answers/<int:question_id>', methods=['GET'])
@require_auth
def api_get_answer_by_question_id(question_id):
    """Restituisce la risposta associata a una domanda."""
    service = ChatService(request)
    response_dto = service.get_answer_by_question_id(question_id)
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status