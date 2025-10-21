from pydantic import BaseModel

class GetQuestionByIdQuery(BaseModel):
    """Query per la richiesta di una domanda tramite ID."""
    question_id: int

class ListQuestionsByUserIdQuery(BaseModel):
    """Query per la richiesta di lista domande utente."""
    user_id: int

class GetAnswerByQuestionIdQuery(BaseModel):
    """Query per la richiesta di una answer tramite ID domanda."""
    question_id: int
