from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta

SECRET_KEY = "your-secret"

def create_verification_token(email):
    return jwt.encode({"email": email, "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")

def create_download_token(file_id, client_id):
    return jwt.encode({"file_id": file_id, "client_id": client_id, "exp": datetime.utcnow() + timedelta(minutes=15)}, SECRET_KEY, algorithm="HS256")

def verify_download_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")