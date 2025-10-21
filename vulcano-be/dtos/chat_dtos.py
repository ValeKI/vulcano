from pydantic import BaseModel
from typing import List, Any, Optional

class QuestionResponseDTO(BaseModel):
    id: int
    content: str
    user_id: int
    content_file_id: Optional[str]
    created_at: Any

class ListQuestionsResponseDTO(BaseModel):
    questions: List[dict]

class InsertQuestionResponseDTO(BaseModel):
    id: int
    question: str
    answer: Any
    file_ids: List[Any]

class AnswerResponseDTO(BaseModel):
    id: int
    question_id: int
    content: str
    content_file_id: Optional[str]
    created_at: Any
