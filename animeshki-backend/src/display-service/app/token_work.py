from datetime import datetime
import jwt
import os
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = str(os.getenv("SECRET_KEY"))

ALGORITHM = "HS256"

def verify_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    expire = payload.get("exp")
    if datetime.fromtimestamp(expire) < datetime.now():
        return False
    return True

def refresh_access_token()