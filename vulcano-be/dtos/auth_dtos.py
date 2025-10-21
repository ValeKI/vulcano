from pydantic import BaseModel

class UserDTO(BaseModel):
    username: str
    email: str

class LoginResponseDTO(BaseModel):
    token: str
    user: UserDTO
    refresh_token: str = None

class RefreshResponseDTO(BaseModel):
    token: str

class CheckResponseDTO(BaseModel):
    status: str
    user: dict

class SignUpResponseDTO(BaseModel):
    status: str
    user: dict

class ForgotPasswordResponseDTO(BaseModel):
    status: str

class ResetPasswordResponseDTO(BaseModel):
    status: str
