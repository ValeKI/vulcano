from pydantic import BaseModel
from typing import List, Any, Optional

class QuestionResponseDTO(BaseModel):
    """DTO per la risposta di una singola domanda."""
    id: int
    content: str
    user_id: int
    content_file_id: Optional[str]
    created_at: Any

class ListQuestionsResponseDTO(BaseModel):
    """DTO per la risposta di lista domande utente."""
    questions: List[dict]

class InsertQuestionResponseDTO(BaseModel):
    """DTO per la risposta di inserimento domanda."""
    id: int
    question: str
    answer: Any
    file_ids: List[Any]

class AnswerResponseDTO(BaseModel):
    """DTO per la risposta di una singola answer."""
    id: int
    question_id: int
    content: str
    content_file_id: Optional[str]
    created_at: Any
