from flask import Request
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
from utils.ai_utils import call_ai_to_generate_answer
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
        """
        question = get_question_by_id(question_id)
        if question:
            return question
        return {"error": "Question not found"}

    def list_questions_by_user_id(self):
        """
        Restituisce la lista delle domande per l'utente corrente.
        Returns:
            dict: Lista domande.
        """
        user_id = get_user_id_from_request()
        questions = list_questions_by_user_id(user_id)
        return {"questions": questions}

    def insert_question(self):
        """
        Inserisce una nuova domanda e genera la risposta.
        Returns:
            dict: Dettagli domanda/risposta.
        """
        data = self.request.json
        content = data.get('content')
        user_id = get_user_id_from_request()

        files_ids = list_files_for_user(user_id)
        if not files_ids:
            return {"error": "Nessun file disponibile per l'utente"}

        ai_answer = read_from_redis_cache(user_id, content)
        if not ai_answer:
            ai_answer = call_ai_to_generate_answer(content, user_id)
            question_id = insert_question(user_id, content)
            answer_id = insert_answer(question_id, ai_answer["answer"])
            for file_id in ai_answer["file_ids"]:
                add_answer_id_to_file_chunks(file_id, answer_id)
            write_to_redis_cache(user_id, content, ai_answer, ai_answer["file_ids"], question_id, answer_id)
        else:
            question_id = ai_answer.get("question_id")
            answer_id = ai_answer.get("answer_id")

        return {
            "id": question_id,
            "question": content,
            "answer": ai_answer,
            "file_ids": ai_answer["file_ids"]
        }

    def get_answer_by_question_id(self, question_id: int):
        """
        Restituisce la risposta associata a una domanda.
        Args:
            question_id (int): ID della domanda.
        Returns:
            dict: Risposta.
        """
        answer = get_answer_by_question_id(question_id)
        if answer:
            return answer
        return {"error": "Answer not found"}
