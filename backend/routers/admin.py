from fastapi import APIRouter,status,Request, HTTPException
from oauth2 import verify_access_token
from database import delete_user, connection_pool, query_username, get_user_posts
from mysql.connector import PoolError
import os

# File that contains all end points related to user administration.  

router = APIRouter(prefix="/admin", tags=["admin"])

# This is the api end point for deleting a user and everything associated
@router.delete("/delete_user/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete(username,request:Request):
    try:
        # Grab the user's token and verify it
        token = request.headers.get('token')
        userData = verify_access_token(token)

        # Check for a valid username, valud data, and ensure the user is not an admin, cant delete admins as of yet.
        if not username:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="field empty")

        if not userData:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        
        if int(userData['permissions']) < 150:
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        
        # Grab all of the user's details and delete their profile picture from the server.
        userDB = query_username(connection_pool, username)
        os.remove('./profile_pictures/'+userDB[5])

        # Grab any posts associated with the user
        userPosts = get_user_posts(connection_pool,userDB[0])

        # If the user has any posts, remove all of them and the attached images,
        # This will automatically delete comments since they will cascade
        # when the post is deleted.
        if userPosts:

            # iterate through all the posts and delete their attachments
            for _,post in enumerate(userPosts):
                os.remove('./attachments/' + post[3])

        # Finally run the query to delete the instance of the user from the database.
        result = delete_user(connection_pool,username)

        # If the delete query returned an error, return a HTTP 500 code.
        if isinstance(result, PoolError):
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR)

        # If no result was returned, then the user does not exist, return a HTTP 400 code.
        if not result:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User does not exist")

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
