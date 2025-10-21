from pydantic import BaseModel

class InsertQuestionCommand(BaseModel):
    """Command per la richiesta di inserimento domanda."""
    content: str
