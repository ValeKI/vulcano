from flask import Request
from dtos.common_dtos import ErrorResponseDTO
from dtos.chat_dtos import QuestionResponseDTO, ListQuestionsResponseDTO, InsertQuestionResponseDTO, AnswerResponseDTO
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
from utils.redis_utils import RedisUtils
from utils.qdrant_utils import QdrantUtils
from utils.ai_utils import AIUtils
from utils.auth_utils import get_user_id_from_request

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
        """
        Restituisce una domanda tramite ID.
        Args:
            question_id (int): ID della domanda.
        Returns:
            dict: Domanda.
            DTO: QuestionResponseDTO, ErrorResponseDTO
        """
        question = get_question_by_id(question_id)
        if question:
            return QuestionResponseDTO(**question)
        return ErrorResponseDTO(error="Question not found")

    def list_questions_by_user_id(self):
        """
        Restituisce la lista delle domande per l'utente corrente.
        Returns:
            dict: Lista domande.
            DTO: ListQuestionsResponseDTO
        """
        user_id = get_user_id_from_request()
        questions = list_questions_by_user_id(user_id)
        return ListQuestionsResponseDTO(questions=questions)

    def insert_question(self):
        """
        Inserisce una nuova domanda e genera la risposta.
        Returns:
            dict: Dettagli domanda/risposta.
            DTO: InsertQuestionResponseDTO, ErrorResponseDTO
        """
        data = self.request.json
        content = data.get('content')
        user_id = get_user_id_from_request()

        files_ids = list_files_for_user(user_id)
        if not files_ids:
            return ErrorResponseDTO(error="Nessun file disponibile per l'utente")

        redis_utils = RedisUtils()
        ai_utils = AIUtils()
        qdrant_utils = QdrantUtils()
        ai_answer = redis_utils.read_from_redis_cache(user_id, content)
        if not ai_answer:
            ai_answer = ai_utils.call_ai_to_generate_answer(content, user_id)
            question_id = insert_question(user_id, content)
            answer_id = insert_answer(question_id, ai_answer["answer"])
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
        """
        Restituisce la risposta associata a una domanda.
        Args:
            question_id (int): ID della domanda.
        Returns:
            dict: Risposta.
            DTO: AnswerResponseDTO, ErrorResponseDTO
        """
        answer = get_answer_by_question_id(question_id)
        if answer:
            return AnswerResponseDTO(**answer)
        return ErrorResponseDTO(error="Answer not found")
