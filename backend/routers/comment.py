from fastapi import APIRouter,status, Request, HTTPException
from schemas import Comment
from oauth2 import verify_access_token
from database import *
from mysql.connector import PoolError

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
def comment(comment: Comment, request: Request):
    try:
        if not comment.comment:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail="Comment field can't be empty")

        comment = comment.comment.strip()

        if len(comment) > 500:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="Comment can't exceed 500 characters")
        
        token = request.headers.get('token')

        postId = request.headers.get('postId')

        if not postId:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        userData = verify_access_token(token)

        if not userData:
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        
        result = create_comment(connection_pool,postId,userData['username'],comment)

        if isinstance(result, PoolError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get('/get/{post_id}', status_code=status.HTTP_200_OK)
def comments(post_id):
    try:
        results = get_post_comments(connection_pool,post_id)

        if not results:
            raise HTTPException(status.HTTP_204_NO_CONTENT)

        return results
    
    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def delete(id, request:Request):
    try:
        token = request.headers.get('token')

        userData = verify_access_token(token)

        commentData = get_comment(connection_pool,id)

        if not commentData:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        if commentData[0][2] != userData['username']:
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        
        result = delete_comment(connection_pool,id)

        if isinstance(result,PoolError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))