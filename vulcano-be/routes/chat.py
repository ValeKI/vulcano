from flask import Blueprint, request, jsonify
from utils.db.db_question_utils import (
    get_question_by_id,
    list_questions_by_user_id,
    insert_question
)
from utils.auth_utils import get_user_id_from_request

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/questions/<int:question_id>', methods=['GET'])
def api_get_question_by_id(question_id):
    question = get_question_by_id(question_id)
    if question:
        return jsonify(question)
    return jsonify({"error": "Question not found"}), 404

@chat_bp.route('/questions/user', methods=['GET'])
def api_list_questions_by_user_id():
    user_id = get_user_id_from_request()
    questions = list_questions_by_user_id(user_id)
    return jsonify({"questions": questions})

@chat_bp.route('/questions', methods=['POST'])
def api_insert_question():
    data = request.json
    content = data.get('content')
    user_id = get_user_id_from_request()
    question_id = insert_question(user_id, content)
    return jsonify({"id": question_id})