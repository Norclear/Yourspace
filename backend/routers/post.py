from fastapi import APIRouter, status, HTTPException, Request
import schemas
from utility import *
import database
from oauth2 import verify_access_token
from mysql.connector import PoolError

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, request: Request):
    try:
        token = request.headers.get('token')

        userData = verify_access_token(token)

        if not userData:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        file_name = ''

        title = post.title

        description = post.description

        if title is None or title.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Title cannot be empty")

        if description is None or description.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Description cannot be empty")

        title = post.title.strip()

        description = post.description.strip()

        if len(title) > 25:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Title can't be more than 25 characters")

        if len(description) > 500:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Description can't be more than 500 characters")

        if post.attachment:

            extension = post.attachment.split(';')[0].split(':')[
                1].split('/')[1]

            encoded_image = (post.attachment.split(';')[1]).split(',')[1]

            if check_image_size(encoded_image):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Image can't be larger than 2MB")

            file_name = str(generate_unique_filename()) + '.' + str(extension)

            compressed_image = compress_image(encoded_image, extension)

            with open(f"attachments/{file_name}", "wb") as f:
                f.write(decode_to_image(compressed_image))

        result = database.create_post(
            database.connection_pool, userData['id'], post.title, post.description, file_name, post.private)

        if isinstance(result, PoolError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.get("/get_post/{id}", status_code=status.HTTP_200_OK)
def get_post(id, request: Request):
    try:
        userData = verify_access_token(request.headers.get('token'))

        postData = database.get_post_by_id(database.connection_pool, id)

        if postData == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if postData[4] == True and postData[5] != userData['username']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        img_data = None

        if postData[2]:
            image = open(f'attachments/{postData[2]}', 'rb')
            image = image.read()
            encoded_image = encode_to_base64(image)
            decompressed_image = decompress_image(encoded_image)
            img_data = {
                "base64": decompressed_image,
                "extension": postData[2].split('.')[1]
            }

        return {"title": postData[0],
                "description": postData[1],
                "attachment": img_data,
                "postDate": postData[3],
                "ownerUsername": postData[5]
                }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.get("/my_posts", status_code=status.HTTP_200_OK)
def my_posts(request: Request):
    try:
        userData = verify_access_token(request.headers.get('token'))

        if not userData:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        posts = database.get_user_posts(
            database.connection_pool, userData['id'])

        if not posts:
            raise HTTPException(status.HTTP_204_NO_CONTENT)

        response = []

        for _, v in enumerate(posts):

            post = {
                'postId': v[0],
                'title': v[1],
                'description': v[2],
                'date': v[4]
            }

            response.append(post)

        return response

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.get('/feed', status_code=status.HTTP_200_OK)
def feed():
    try:
        posts = database.get_feed(database.connection_pool)

        if not posts:
            raise HTTPException(status.HTTP_204_NO_CONTENT)

        return posts

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.put('/edit/{id}', status_code=status.HTTP_200_OK)
def edit_post(id, postEdit: schemas.PostEdit, request: Request):
    try:
        token = request.headers.get('token')

        userData = verify_access_token(token)

        if not userData:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        postData = database.get_post_by_id(database.connection_pool, id)

        # 2nd check. post should exist since a get_post was run when the edit page was opened but it is possble someone may delete it by the time this request is made
        if not postData:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        if postData[5] != userData['username']:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        if postEdit.title is None or postEdit.title.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Title cannot be empty")

        if postEdit.description is None or postEdit.description.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Description cannot be empty")

        title = postEdit.title.strip()

        description = postEdit.description.strip()

        if len(title) > 25:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail="Title can't be more than 25 characters")

        if len(description) > 500:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail="Description can't be more than 500 characters")

        # if a user submitted a edit with no changes we simply returna 200 so we dont peform a sql edit/query for no reason
        if postData[0] == title and postData[1] == description:
            raise HTTPException(status.HTTP_200_OK)

        result = database.update_post(
            database.connection_pool, id, postEdit.title, postEdit.description)

        if isinstance(result, PoolError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id, request: Request):
    try:
        userData = verify_access_token(request.headers.get('token'))

        postData = (database.get_post_by_id(database.connection_pool, id))

        if postData == None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        if not postData[5] == userData['username']:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        result = database.delete_post(database.connection_pool, id)

        if isinstance(result, PoolError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

        if postData[2]:
            delete_image('attachments/' + postData[2])

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
