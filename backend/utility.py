from passlib.context import CryptContext
import base64
import uuid
from PIL import Image
import io
import requests
import random
from database import connection_pool, get_pfp
import os

# This is an important file, it contains all key utility functions that are crucial to the server.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hash the password inputted by the user
def hash(password: str): 
    return pwd_context.hash(password)

#compare the hashed password versus the stored hash password to verify the user has inputted the correct password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#convert an image into a base64 string to store it in a database
def decode_to_image(encoded_image):
    return base64.b64decode(encoded_image)

#convert a base64 string into an image to return to the client
def encode_to_base64(decoded_image):
    return base64.b64encode(decoded_image)

#randomly generate a completely unique string to store images. 64 bit strings ensure that the likelyhood of strings being identical is pratically impossible
def generate_unique_filename():
    return str(uuid.uuid4())

#compress the image (in a base64 string) for the purposes of storing it in the file system. The compression is of the lossy type and converts the image into a jpeg file
def compress_image(image_data, extension, quality: int = 30):
    image_data = base64.b64decode(image_data)
    img = Image.open(io.BytesIO(image_data))
    output = io.BytesIO()
    img.save(output, format=extension, quality=quality)
    compressed_img_data = output.getvalue()
    return base64.b64encode(compressed_img_data).decode()

#partially reverse the image compression to return it to the client
def decompress_image(image_data, quality: int = 100):
    image_data = base64.b64decode(image_data)
    img = Image.open(io.BytesIO(image_data))
    output = io.BytesIO()
    img.save(output, format=img.format, quality=quality)
    decompressed_img_data = output.getvalue()
    return base64.b64encode(decompressed_img_data).decode()

#generate a random hex colour code
def random_hex_color():
    return ''.join(hex(random.randint(0, 15))[2:] for _ in range(6))

#generate the unique user profile pictures using a random seed and the dice bear api and then save it to the filesystem
def generate_pfp(seed):
    style = 'bottts'
    radius = 25
    backgroundColor = random_hex_color()
    backgroundType = 'gradientLinear'
    mouthProbability = 100
    sidesProbability = 50
    textureProbability = 50
    topProbability = 70
    size = 64 
    response = requests.get(
        f'https://api.dicebear.com/5.x/{style}/svg?seed={seed}&radius={radius}&backgroundColor={backgroundColor}&backgroundType={backgroundType}&mouthProbability={mouthProbability}&sidesProbability={sidesProbability}&textureProbability={textureProbability}&topProbability={topProbability}&size={size}')

    fileName = generate_unique_filename()

    with open(f'profile_pictures/${fileName}.svg', "wb") as f:
      f.write(response.content)

    return f'${fileName}.svg'

#perform a range check of the image that is uploaded by the client to ensure it is under the 2MB limit. this check is also performed client side.
def check_image_size(image_base64):
    image_bytes = base64.b64decode(image_base64)
    if len(image_bytes) > 2 * 1024 * 1024:
        return True
    return False

#returns the profile picture of the user to add to their navbar as they navigate the site.
def get_picture(username):
    picture_location = get_pfp(connection_pool, username)

    with open(f'profile_pictures/{picture_location[0]}', "r") as f:
            contents = f.read()

    return contents

#deletes an image saved in the file system
def delete_image(path):
    os.remove(path)