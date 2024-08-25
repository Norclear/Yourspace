from fastapi import status, APIRouter, Request, HTTPException, status
from schemas import UserCreate
import database
import utility
import re
from mysql.connector import PoolError

router = APIRouter(prefix="/users", tags=["Users"])

# Api end point for creating a user
@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def createUser(user: UserCreate):
    try:

        # Strip the user inputted username of exessive whitespace
        user.username = user.username.strip()
        
        # If the username is black, return a 400
        if user.username == "": # check the client has entered a username
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username cannot be empty")
        
        # If the password is blank, return a 400
        if user.password == "": # check the client has entered a password
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password cannot be empty")
        
        # Perform all the minumum requirement checks for the user passwords and usernames
        if len(user.username) < 6: # check the requested username is atleast or more than 6 chracters
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username is too short")

        if len(user.username) > 14: # check the requested username is equal to or less than 14 characters
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username is too long")

        if re.search("\W", user.username): # check the requested username only contains a-Z 0-9 and _ | reference for regex https://www.w3schools.com/python/python_regex.asp
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Characters a-Z, 0-9 and _<br>allowed in username")

        if len(user.password) < 8: # check user password is atleast or more than 8 characters 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password is too short")
        
        if len(user.password) > 64:  # check user password is no more than 64 (Database limitation)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password is too long")
        
        # Ensure the chosen username is not already taken
        username_exists = database.query_username(database.connection_pool,user.username) # query database as to wether the username is taken

        if username_exists: # return bad request if username is taken
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username is taken")
        
        # Hash the user's password before storing it
        user.password = utility.hash(user.password) # hash the users password see utility.py for functions

        # Generate a unique profile picture for the user
        user.pfp = utility.generate_pfp(user.username)

        # Query the database to insert the new user instance
        result = database.create_user(database.connection_pool,user) # if all checks passed user will be generated in database, see database.py for database functions
        
        if isinstance(result,PoolError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    except HTTPException:
        raise
        
    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

# sorta deperecated, at the moment all home stuff is frontend since everything displayed on the home page is stored in the client side JWT token
@router.get("/home", status_code=status.HTTP_200_OK) 
def home(request: Request):
    # access_token = request.headers.get('token')
    # userData = verify_access_token(access_token)

    # if userData == False:
    #     return False

    # del userData['expiry']
    # return {'token': userData}
    pass

# Api end point for user's personal pages
@router.get("/user/{username}", status_code=status.HTTP_200_OK)
def view_user(username: str):
    try:

        # Query the database to the account requested
        userData = database.query_account(database.connection_pool,username)
        
        # Check the user exists
        if userData == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        return userData

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
