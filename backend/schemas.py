from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pydantic.types import conint


class PostBase(BaseModel):
    title: str = None
    description: str = None
    attachment: str = None
    private: bool = None

class PostCreate(PostBase):
    pass

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


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class PostEdit(BaseModel):
    title: str
    description: str


class UserCreate(BaseModel):
    username: str
    password: str
    permissions: int = 100
    pfp: str = None


class UserLogin(BaseModel):
    username: str
    password: str

class Comment(BaseModel):
    comment: str = None


