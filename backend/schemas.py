from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pydantic.types import conint

# This is a base class for all posts
class PostBase(BaseModel):
    title: str = None
    description: str = None
    attachment: str = None
    private: bool = None

class PostCreate(PostBase):
    pass

# Base class for JWT tokens
class Token(BaseModel):
    token: str

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

# Class for the details of a post to be seen on the site
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

# Class for editing posts
class PostEdit(BaseModel):
    title: str
    description: str

# Class for creating new users, permissions are set to a default of 100.
class UserCreate(BaseModel):
    username: str
    password: str
    permissions: int = 100
    pfp: str = None

# Class for users logging in.
class UserLogin(BaseModel):
    username: str
    password: str

class Comment(BaseModel):
    comment: str = None


