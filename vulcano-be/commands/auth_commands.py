from pydantic import BaseModel

class LoginCommand(BaseModel):
    usernameOrEmail: str
    password: str

class SignUpCommand(BaseModel):
    username: str
    email: str
    password: str

class ForgotPasswordCommand(BaseModel):
    email: str

class ResetPasswordCommand(BaseModel):
    token: str
    new_password: str
