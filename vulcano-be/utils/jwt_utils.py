import jwt
from datetime import datetime, timedelta, timezone
from config import CURRENT_CONFIG

SECRET_KEY = CURRENT_CONFIG.SECRET_KEY
REFRESH_SECRET_KEY = CURRENT_CONFIG.REFRESH_SECRET_KEY

def generate_access_token(payload: dict, expires_in: int = 86400):
    payload_copy = payload.copy()
    payload_copy["exp"] = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    token = jwt.encode(payload_copy, SECRET_KEY, algorithm="HS256")
    return token

def generate_refresh_token(payload: dict, expires_in: int = 60 * 60 * 24 * 7):  # 7 giorni
    print("Generated refresh token in utils - input payload:", payload)
    data = payload.copy()
    data["exp"] = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    x = jwt.encode(data, REFRESH_SECRET_KEY, algorithm="HS256")
    print("Generated refresh token in util:", x)
    return x

def verify_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError as e:
        return None
    except jwt.InvalidTokenError as e:
        return None

def verify_refresh_token(token: str):
    try:
        decoded = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError as e:
        return None
    except jwt.InvalidTokenError as e:
        return None

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])