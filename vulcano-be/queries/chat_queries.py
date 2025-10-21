from pydantic import BaseModel

class GetQuestionByIdQuery(BaseModel):
    question_id: int

class ListQuestionsByUserIdQuery(BaseModel):
    user_id: int

class GetAnswerByQuestionIdQuery(BaseModel):
    question_id: int
