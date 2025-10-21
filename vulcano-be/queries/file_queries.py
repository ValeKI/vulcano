from pydantic import BaseModel

class DownloadFileQuery(BaseModel):
    """Query per la richiesta di download file."""
    file_id: str

class ListFilesQuery(BaseModel):
    """Query per la richiesta di lista file utente."""
    pass

class ListFilesByAnswerIdQuery(BaseModel):
    """Query per la richiesta di lista file per answer."""
    answer_id: str
