from pydantic import BaseModel

class RefreshQuery(BaseModel):
    refresh_token: str

class CheckQuery(BaseModel):
    pass
