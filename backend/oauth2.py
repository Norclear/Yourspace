from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
import os
from datetime import datetime, timedelta

# This is an important file since it performs all user authentication related actions such as web related 
# authentication using JWT tokens.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET KEY
SECRET_KEY = os.getenv('secret_key')
# ALGORITHM
ALGORITHM = os.getenv('algorithm')
# TOKEN EXPIRATION
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('access_token_expire_minutes')

# this function generates a access token for the user once they have been authorised. token is of the type 'jwt' JSON web token. it expires are a predetermined time, can be found in .env, and is calculated at 'token expiry' variable. a valid encoded jwt token is returned to the caller. 
def create_token(data: dict):
    encodable = data.copy()

    token_expiry = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    encodable.update({"expiry": str(token_expiry)})

    encoded_token = jwt.encode(encodable,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_token

# The user will need to have their token verified every time they access a new page in order to make sure they authenticated
def verify_access_token(token:str ):

    # Check a token was even sent
    if not token:
        return False
    
    # Attempt to decode the token if it is not possible (user has a malicious/fake token) then return false to the caller
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
    except JWTError:
        return False

    # If the token is verified to be valid then ensure it hasn't expired yet.
    # If it has expired return false, the front end will automatically delete it and 'log them out'
    if datetime.utcnow() >= datetime.strptime(payload['expiry'], '%Y-%m-%d %H:%M:%S.%f'):
        return False
    
    # If the user token passes all tests then return the data stored in the token, including the key user details.
    return payload