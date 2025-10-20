from flask import Blueprint, request, jsonify
from utils.db.db_question_utils import (
    get_question_by_id,
    list_questions_by_user_id,
    insert_question
)
from utils.db.db_answer_utils import (
    insert_answer,
    get_answer_by_question_id
)
from utils.db.db_file_utils import list_files_for_user
from utils.redis_utils import (
    read_from_redis_cache,
    write_to_redis_cache
)
from utils.qdrant_utils import add_answer_id_to_file_chunks
from utils.ai_utils import (
    call_ai_to_generate_answer
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

    files_ids = list_files_for_user(user_id)
    if not files_ids:
        return jsonify({"error": "Nessun file disponibile per l'utente"}), 400


    # gestione su redis in lettura futura (cache delle risposte)
    ai_answer = read_from_redis_cache(content)
    if not ai_answer:
        # chiama AI per generare la risposta alla domanda inserita
        ai_answer = call_ai_to_generate_answer(content, user_id=user_id)

        # salva la risposta nel database
        question_id = insert_question(user_id, content)
        answer_id = insert_answer(question_id, ai_answer["answer"])

        # aggiorna qdrant
        for file_id in ai_answer["file_ids"]:
            add_answer_id_to_file_chunks(file_id, answer_id)

        # gestione su redis in scrittura futura (cache delle risposte)
        write_to_redis_cache(content, ai_answer)

    return jsonify({"id": question_id, "question": content, "answer": ai_answer, "file_ids": ai_answer["file_ids"]})

@chat_bp.route('/answers/<int:question_id>', methods=['GET'])
def api_get_answer_by_question_id(question_id):
    answer = get_answer_by_question_id(question_id)
    if answer:
        return jsonify(answer)
    return jsonify({"error": "Answer not found"}), 404