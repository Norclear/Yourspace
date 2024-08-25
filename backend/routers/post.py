from fastapi import APIRouter, status, HTTPException, Request
import schemas
from utility import *
import database
from oauth2 import verify_access_token
from mysql.connector import PoolError

# This file contains the api end point for posts and their functionality

router = APIRouter(prefix="/posts", tags=["Posts"])

# end point for creating posts
@router.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, request: Request):
    try:

        # Ensure the user has a valid JWT token,
        # first grab it from the header of the request
        # then verify it.
        token = request.headers.get('token')

        userData = verify_access_token(token)

        # If the token is not valid, user is not authorised to create posts, return 401
        if not userData:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        # Initialise a file name variable that will store any attachment if provided
        file_name = ''

        title = post.title

        description = post.description

        # Ensure that a title is provided and also ensure not only whitespaces were provided
        # else return a 400
        if title is None or title.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Title cannot be empty")
        
        # Ensure that a description is provided and also ensure not only whitespaces were provided
        # else return a 400
        if description is None or description.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Description cannot be empty")

        # Then truncate the title for any unnecessary whitespaces
        title = post.title.strip()

        # Likewise for the description
        description = post.description.strip()

        # Ensure the title is less than 25 characters
        if len(title) > 25:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Title can't be more than 25 characters")
        # Ensure the description is less than 500 characters
        if len(description) > 500:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Description can't be more than 500 characters")

        # If an image was provided, we need to extract the base 64
        if post.attachment:

            extension = post.attachment.split(';')[0].split(':')[
                1].split('/')[1]

            encoded_image = (post.attachment.split(';')[1]).split(',')[1]

            # Ensure the image is 2Mb or less
            if check_image_size(encoded_image):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Image can't be larger than 2MB")

            # Generates a name for the file that is totally unique
            file_name = str(generate_unique_filename()) + '.' + str(extension)

            # Compresses the image
            compressed_image = compress_image(encoded_image, extension)

            # Write the image to the disk in the attachments file
            with open(f"attachments/{file_name}", "wb") as f:
                f.write(decode_to_image(compressed_image))

        # Create the post instance in the database
        result = database.create_post(
            database.connection_pool, userData['id'], post.title, post.description, file_name, post.private)

        if isinstance(result, PoolError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

# API end point to return a particular post given it's ID
@router.get("/get_post/{id}", status_code=status.HTTP_200_OK)
def get_post(id, request: Request):
    try:

        # Verify the user's access token and extract the data from the token
        userData = verify_access_token(request.headers.get('token'))
        
        # Query all the data for a post using the post ID
        postData = database.get_post_by_id(database.connection_pool, id)

        # If no data exists for the post, return a 404
        if postData == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        # Check the post is marked as private (postData[4]) and the user accessing the post is the owner of the post,
        # if it's private and another user try's to access it, that is forbidden, return a 403
        if postData[4] == True and postData[5] != userData['username']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        # Declare an empty variable for the image data
        img_data = None

        # If the post has an attached image,
        if postData[2]:

            # Proceed to opening the file and reading it as a binary
            image = open(f'attachments/{postData[2]}', 'rb')
            image = image.read()
            
            # Encode the image from binary to base64 format to allow us to transport it
            encoded_image = encode_to_base64(image)

            decompressed_image = decompress_image(encoded_image)

            # Encode the image as a JSON string
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

# API End point that returns all posts for a specific user
@router.get("/my_posts", status_code=status.HTTP_200_OK)
def my_posts(request: Request):
    try:

        # Verify the user's jwt token and return the data in the token
        userData = verify_access_token(request.headers.get('token'))

        # If no user data is found, return 401
        if not userData:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        # Query the database to get all posts for a specific user
        posts = database.get_user_posts(
            database.connection_pool, userData['id'])

        # If no posts are found return a 204
        if not posts:
            raise HTTPException(status.HTTP_204_NO_CONTENT)

        # Initialise an empty variable to store all the posts
        response = []

        # Loop through the database response and encapsulate all posts into a dictionary,
        # Then append the dictionary to the list
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

# Api end point to get a list of all the posts to return to a user's feed
@router.get('/feed', status_code=status.HTTP_200_OK)
def feed():
    try:

        # Query the data base to get the last 100 posts.
        posts = database.get_feed(database.connection_pool)

        # If no posts are found, return a 404, this would be a sad day :(
        if not posts:
            raise HTTPException(status.HTTP_204_NO_CONTENT)

        return posts

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

# Api end point for editing the details of an existing post
@router.put('/edit/{id}', status_code=status.HTTP_200_OK)
def edit_post(id, postEdit: schemas.PostEdit, request: Request):
    try:

        # Get the user's token
        token = request.headers.get('token')

        # Verify the token and return the user's data
        userData = verify_access_token(token)

        # If userData is false, then access is forbidden, return a 403
        if not userData:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        # Query the database to get the post's details
        postData = database.get_post_by_id(database.connection_pool, id)

        # 2nd check. post should exist since a get_post was run when the edit page was opened but it is possible someone may delete it by the time this request is made
        if not postData:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        # If the user attempting to edit the post is not the owner, return a 403
        if postData[5] != userData['username']:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        # Title checks, same as when we create a post
        if postEdit.title is None or postEdit.title.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Title cannot be empty")
        # Description checks, same as when we create a post
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

        # Query the database to update the instance of the post in the database
        result = database.update_post(
            database.connection_pool, id, postEdit.title, postEdit.description)

        if isinstance(result, PoolError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

# Api end point for deleting a post
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id, request: Request):
    try:

        # Get the user data from the jwt token
        userData = verify_access_token(request.headers.get('token'))

        postData = (database.get_post_by_id(database.connection_pool, id))

        # If the post doesnt exist, return a 404
        if postData == None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        # If the user isn't authorised to delete the post, return a 403
        if not postData[5] == userData['username']:
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        # Query the database to delete the post
        result = database.delete_post(database.connection_pool, id)

        if isinstance(result, PoolError):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

        # If an image is attached, delete it
        if postData[2]:
            delete_image('attachments/' + postData[2])

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
