from fastapi import status, APIRouter, HTTPException, Request, Response
from schemas import UserLogin
from database import *
from utility import verify, get_picture
from oauth2 import create_token, verify_access_token

router = APIRouter(tags=["Authenticator"])


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLogin, response: Response):
    #     response.headers["Access-Control-Allow-Origin"] = "*"
    try:
        # remove trailing and begining whitespaces
        user.username = user.username.strip()

        if user.username == "":  # check the client has entered a username
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username cannot be empty")

        if user.password == "":  # check the client has entered a password
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password cannot be empty")

        username_exists = query_username(
            connection_pool, user.username)

        if not username_exists:  # query the database to check the username and subsequentially the account exists
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Incorrect Credentials")

        # query for the hashed password of the username
        hashed_pass = query_password(connection_pool, user.username)

        # compare the password in the database to the one entered to verify it is correct
        if not verify(user.password, hashed_pass):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Incorrect Credentials")

        id = str(username_to_id(connection_pool, user.username))

        permissions = query_permissions(connection_pool, id)

        print(permissions)

        contents = get_picture(user.username)

        # create an access token for the user in the form of JWT and then return it
        access_token = create_token(
            {"id": id, "username": user.username, "permissions": permissions, "picture": contents})

        return {"token": access_token}

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.get("/verify_token", status_code=status.HTTP_200_OK)
async def verify_token(request: Request, response: Response):
    #     response.headers["Access-Control-Allow-Origin"] = "*"
    try:
        access_token = request.headers.get('token')
        userData = verify_access_token(access_token)
        if userData == False:
            return {"loggedIn": False,
                    "userData": None}

        return {"loggedIn": True,
                "userData": userData}
    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
