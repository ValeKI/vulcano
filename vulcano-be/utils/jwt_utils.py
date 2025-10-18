import jwt
from datetime import datetime, timedelta
from config import CURRENT_CONFIG

SECRET_KEY = CURRENT_CONFIG.SECRET_KEY

def generate_token(payload: dict, expires_hours=1):
    #payload["exp"] = datetime.utcnow() + timedelta(hours=expires_hours)
    return jwt.encode(payload, CURRENT_CONFIG.SECRET_KEY, algorithm="HS256")

def decode_token(token: str):
    return jwt.decode(token, CURRENT_CONFIG.SECRET_KEY, algorithms=["HS256"])