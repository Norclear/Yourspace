from fastapi import APIRouter, status, HTTPException, Query
from utility import *
import database

router = APIRouter(tags=["Filter"])


@router.get("/filter", status_code=status.HTTP_200_OK)
async def filter(query: str = Query()):
    try:
        users = database.search_users(database.connection_pool,query)
        posts = database.search_posts(database.connection_pool, query)

        response = {
            'users': [],
            'posts': []
        }


        for _,v in enumerate(users):
            picture = get_picture(v[1])
            user = {
                'username':v[1],
                'picture':picture
            }
            response['users'].append(user)

        for _,v in enumerate(posts):
            if v[6]:
                continue
            post = {
                'postId':v[0],
                'title': v[1],
                'description': v[2],
                'date':v[4]
            }
            response['posts'].append(post)

        if not response['posts'] and not response['users']:
            raise HTTPException(status.HTTP_204_NO_CONTENT)
                
        return response

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(error))