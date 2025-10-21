from flask import Blueprint, request, jsonify
from services.chat_service import ChatService
from utils.auth_utils import get_user_id_from_request
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
    """Restituisce una domanda tramite ID.

    ---
    parameters:
      - name: question_id
        in: path
        type: integer
        required: true
        description: ID della domanda
    responses:
      200:
        description: Domanda trovata
        schema:
          type: object
          properties:
            id:
              type: integer
            content:
              type: string
            user_id:
              type: integer
            content_file_id:
              type: string
            created_at:
              type: string
      404:
        description: Domanda non trovata
        schema:
          type: object
          properties:
            error:
              type: string
    """
    service = ChatService(request)
    response_dto = service.get_question_by_id(question_id)
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@chat_bp.route('/questions/user', methods=['GET'])
@require_auth
def api_list_questions_by_user_id():
    """Restituisce la lista delle domande dell'utente autenticato.

    ---
    responses:
      200:
        description: Lista domande restituita con successo
        schema:
          type: object
          properties:
            questions:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  content:
                    type: string
                  user_id:
                    type: integer
                  content_file_id:
                    type: string
                  created_at:
                    type: string
    """
    service = ChatService(request)
    response_dto = service.list_questions_by_user_id()
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@chat_bp.route('/questions', methods=['POST'])
@require_auth
def api_insert_question():
    """Inserisce una nuova domanda e genera la risposta.

    ---
    parameters:
      - name: content
        in: body
        required: true
        schema:
          type: object
          properties:
            content:
              type: string
    responses:
      200:
        description: Domanda e risposta generate con successo
        schema:
          type: object
          properties:
            id:
              type: integer
            question:
              type: string
            answer:
              type: object
            file_ids:
              type: array
              items:
                type: string
      400:
        description: Nessun file disponibile per l'utente
        schema:
          type: object
          properties:
            error:
              type: string
    """
    service = ChatService(request)
    response_dto = service.insert_question()
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status

@chat_bp.route('/answers/<int:question_id>', methods=['GET'])
@require_auth
def api_get_answer_by_question_id(question_id):
    """Restituisce la risposta associata a una domanda.

    ---
    parameters:
      - name: question_id
        in: path
        type: integer
        required: true
        description: ID della domanda
    responses:
      200:
        description: Risposta trovata
        schema:
          type: object
          properties:
            id:
              type: integer
            question_id:
              type: integer
            content:
              type: string
            content_file_id:
              type: string
            created_at:
              type: string
      404:
        description: Risposta non trovata
        schema:
          type: object
          properties:
            error:
              type: string
    """
    service = ChatService(request)
    response_dto = service.get_answer_by_question_id(question_id)
    status = get_status_code(response_dto)
    return jsonify(response_dto.model_dump()), status