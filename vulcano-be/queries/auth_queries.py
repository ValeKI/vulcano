from pydantic import BaseModel

class RefreshQuery(BaseModel):
    """Query per la richiesta di refresh token."""
    refresh_token: str

class CheckQuery(BaseModel):
    """Query per la richiesta di verifica utente."""
    pass
