from pydantic import BaseModel

class InsertQuestionCommand(BaseModel):
    content: str
