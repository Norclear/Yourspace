from fastapi import APIRouter,status, Request, HTTPException
from schemas import Comment
from oauth2 import verify_access_token
from database import *
from mysql.connector import PoolError

# This file is the API end point for all comments and their functionality

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
def comment(comment: Comment, request: Request):
    try:
        # Check that the comment body was provided with text
        if not comment.comment:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail="Comment field can't be empty")

        # Truncate any unnecassary whitespaces  
        comment = comment.comment.strip()

        # Ensure the comment is less than 500 characters
        if len(comment) > 500:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="Comment can't exceed 500 characters")

        # Grba the user's JWT token
        token = request.headers.get('token')

        # Grab the token of the post that's being commented on
        postId = request.headers.get('postId')

        # If no post ID is found, return a 404
        if not postId:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        # Verify the user's JWT token
        userData = verify_access_token(token)

        # If their token is not valid, they can't comment, return a 403
        if not userData:
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        
        # Insert the comment into the database
        result = create_comment(connection_pool,postId,userData['username'],comment)

        # If the query returns an error, return a 500
        if isinstance(result, PoolError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

# End point to get all the comments on a  post
@router.get('/get/{post_id}', status_code=status.HTTP_200_OK)
def comments(post_id):
    try:
        
        # Get all the commends on the post by querying the database
        results = get_post_comments(connection_pool,post_id)

        # If no comments are found, return a 204, note this is not
        # the same as a 404 nor is it an error
        if not results:
            raise HTTPException(status.HTTP_204_NO_CONTENT)

        return results
    
    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

# End point to delete a comment 
@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def delete(id, request:Request):
    try:

        # Grab the token from the request header
        token = request.headers.get('token')

        # grab the user data from the token
        userData = verify_access_token(token)

        # get all the comments for the post
        commentData = get_comment(connection_pool,id)

        # If no such comment exists, return 404, not sure how this could happen tho
        if not commentData:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        # If the comment doesnt belong to the user, return a 403
        if commentData[0][2] != userData['username']:
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        
        # Query to delete the comment from the database
        result = delete_comment(connection_pool,id)

        if isinstance(result,PoolError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))