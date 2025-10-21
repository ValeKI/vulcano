from pydantic import BaseModel
from typing import List

class UploadFileResponseDTO(BaseModel):
    status: str
    filename: str

class DownloadFileResponseDTO(BaseModel):
    file_data: bytes
    file_name: str

class ListFilesResponseDTO(BaseModel):
    files: List[dict]

class ListFilesByAnswerIdResponseDTO(BaseModel):
    files: List[dict]
