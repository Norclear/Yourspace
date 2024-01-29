from fastapi import APIRouter,status,Request, HTTPException
from oauth2 import verify_access_token
from database import delete_user, connection_pool, query_username, get_user_posts
from mysql.connector import PoolError
import os

router = APIRouter(prefix="/admin", tags=["admin"])


@router.delete("/delete_user/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete(username,request:Request):
    try:
        token = request.headers.get('token')
        userData = verify_access_token(token)

        if not username:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="field empty")

        if not userData:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        
        if int(userData['permissions']) < 150:
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        
        
        userDB = query_username(connection_pool, username)
        os.remove('./profile_pictures/'+userDB[5])

        userPosts = get_user_posts(connection_pool,userDB[0])

        if userPosts:
            for i,v in enumerate(userPosts):
                os.remove('./attachments/'+v[3])

        result = delete_user(connection_pool,username)

        if isinstance(result, PoolError):
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not result:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User does not exist")

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
