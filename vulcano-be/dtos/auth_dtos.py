from pydantic import BaseModel

class UserDTO(BaseModel):
    """DTO per i dati utente restituiti nelle risposte."""
    username: str
    email: str

class LoginResponseDTO(BaseModel):
    """DTO per la risposta di login."""
    token: str
    user: UserDTO
    refresh_token: str | None

class RefreshResponseDTO(BaseModel):
    """DTO per la risposta di refresh token."""
    token: str

class CheckResponseDTO(BaseModel):
    """DTO per la risposta di verifica utente."""
    status: str
    user: dict

class SignUpResponseDTO(BaseModel):
    """DTO per la risposta di registrazione utente."""
    status: str
    user: dict

class ForgotPasswordResponseDTO(BaseModel):
    """DTO per la risposta di richiesta reset password."""
    status: str

class ResetPasswordResponseDTO(BaseModel):
    """DTO per la risposta di reset password."""
    status: str
