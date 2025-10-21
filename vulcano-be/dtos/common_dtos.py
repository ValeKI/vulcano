from pydantic import BaseModel

class ErrorResponseDTO(BaseModel):
    """DTO per la risposta di errore standard."""
    error: str
