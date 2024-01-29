from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET KEY
SECRET_KEY = os.getenv('secret_key')
# ALGORITHM
ALGORITHM = os.getenv('algorithm')
# TOKEN EXPIRATION
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('access_token_expire_minutes')

 # this function generates a access token for the user once they have been authorised. token is of the type 'jwt' JSON web token. it expires are a predetermined time, can be found in .env, and is calculated at 'token expiry' variable. a valid encoded jwt token is returned to the caller. \/

def create_token(data: dict):
    encodable = data.copy()

    token_expiry = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    encodable.update({"expiry": str(token_expiry)})

    encoded_token = jwt.encode(encodable,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_token

def verify_access_token(token:str ):

    if not token:
        return False
    
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
    except JWTError:
        return False

    if datetime.utcnow() >= datetime.strptime(payload['expiry'], '%Y-%m-%d %H:%M:%S.%f'):
        return False
    

    return payload