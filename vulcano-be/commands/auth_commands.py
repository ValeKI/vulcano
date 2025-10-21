from pydantic import BaseModel

class LoginCommand(BaseModel):
    """Command per la richiesta di login."""
    usernameOrEmail: str
    password: str

class SignUpCommand(BaseModel):
    """Command per la richiesta di registrazione utente."""
    username: str
    email: str
    password: str

class ForgotPasswordCommand(BaseModel):
    """Command per la richiesta di reset password."""
    email: str

class ResetPasswordCommand(BaseModel):
    """Command per la richiesta di aggiornamento password."""
    token: str
    new_password: str
