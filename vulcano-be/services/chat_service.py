from flask import Request, jsonify
from dtos.common_dtos import ErrorResponseDTO
from dtos.chat_dtos import QuestionResponseDTO, ListQuestionsResponseDTO, InsertQuestionResponseDTO, AnswerResponseDTO
from utils.db.db_question_utils import DbQuestionUtils
from utils.db.db_answer_utils import DbAnswerUtils
from utils.db.db_file_utils import DbFileUtils
from utils.redis_utils import RedisUtils
from utils.qdrant_utils import QdrantUtils
from utils.ai_utils import AIUtils
from utils.auth_utils import AuthUtils

class ChatService:
    """
    Service per la gestione delle domande e risposte della chat.
    """

    def __init__(self, request: Request):
        """
        Inizializza il service con la richiesta Flask.
        Args:
            request (Request): Oggetto request Flask.
        """
        self.request = request

    def get_question_by_id(self, question_id: int):
        db_question_utils = DbQuestionUtils()
        question = db_question_utils.get_question_by_id(question_id)
        if question:
            return QuestionResponseDTO(**question)
        return ErrorResponseDTO(error="Question not found")

    def list_questions_by_user_id(self):
        auth_utils = AuthUtils(self.request)
        db_question_utils = DbQuestionUtils()
        user_id = auth_utils.get_user_id_from_request()
        if user_id is None:
            return jsonify({"error": "Utente non autorizzato"}), 401
        questions = db_question_utils.list_questions_by_user_id(user_id)
        return ListQuestionsResponseDTO(questions=questions)

    def insert_question(self):
        data = self.request.json
        content = data.get('content')
        auth_utils = AuthUtils(self.request)
        db_question_utils = DbQuestionUtils()
        db_answer_utils = DbAnswerUtils()
        db_file_utils = DbFileUtils()
        user_id = auth_utils.get_user_id_from_request()
        if user_id is None:
            return jsonify({"error": "Utente non autorizzato"}), 401

        files_ids = db_file_utils.list_files_for_user(user_id)
        if not files_ids:
            return ErrorResponseDTO(error="Nessun file disponibile per l'utente")

        redis_utils = RedisUtils()
        ai_utils = AIUtils()
        qdrant_utils = QdrantUtils()
        ai_answer = redis_utils.read_from_redis_cache(user_id, content)
        if not ai_answer:
            ai_answer = ai_utils.call_ai_to_generate_answer(content, user_id)
            question_id = db_question_utils.insert_question(user_id, content)
            answer_id = db_answer_utils.insert_answer(question_id, ai_answer["answer"])
            for file_id in ai_answer["file_ids"]:
                qdrant_utils.add_answer_id_to_file_chunks(file_id, answer_id)
            redis_utils.write_to_redis_cache(user_id, content, ai_answer, ai_answer["file_ids"], question_id, answer_id)
        else:
            question_id = ai_answer.get("question_id")
            answer_id = ai_answer.get("answer_id")

        return InsertQuestionResponseDTO(
            id=question_id,
            question=content,
            answer=ai_answer,
            file_ids=ai_answer["file_ids"]
        )

    def get_answer_by_question_id(self, question_id: int):
        db_answer_utils = DbAnswerUtils()
        answer = db_answer_utils.get_answer_by_question_id(question_id)
        if answer:
            return AnswerResponseDTO(**answer)
        return ErrorResponseDTO(error="Answer not found")
