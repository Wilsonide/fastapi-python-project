from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class Post_create(BaseModel):
    title: str
    published: Optional[bool]
    content: str


class User(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Post(Post_create):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post:Post
    votes: int 
    class Config:
        orm_mode = True



class User_create(BaseModel):
    email: EmailStr
    password: str


class User_login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Token_data(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: bool
