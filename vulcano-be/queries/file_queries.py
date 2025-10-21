from pydantic import BaseModel

class DownloadFileQuery(BaseModel):
    file_id: str

class ListFilesQuery(BaseModel):
    pass

class ListFilesByAnswerIdQuery(BaseModel):
    answer_id: str
