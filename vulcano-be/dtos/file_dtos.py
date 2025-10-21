from pydantic import BaseModel
from typing import List

class UploadFileResponseDTO(BaseModel):
    """DTO per la risposta di upload file."""
    status: str
    filename: str

class DownloadFileResponseDTO(BaseModel):
    """DTO per la risposta di download file."""
    file_data: bytes
    file_name: str

class ListFilesResponseDTO(BaseModel):
    """DTO per la risposta di lista file utente."""
    files: List[dict]

class ListFilesByAnswerIdResponseDTO(BaseModel):
    """DTO per la risposta di lista file per answer."""
    files: List[dict]
