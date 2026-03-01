from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
# class Post(BaseModel):
    # title:str
    # content:str
    # published:bool =True


class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode=True
    



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id:int
    user_id:int
    user:UserOut
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id:Optional[int]=None


class Vote(BaseModel):
    post_id:int
    dir:bool


class PostOut(BaseModel):
    Post:PostResponse
    votes:int


    class Config:
        from_attributes = True
    


# class CreatePost(BaseModel):
#     title:str
#     content:str
#     published:bool =True



# class UpdatePost(BaseModel):
#     title:str
#     content:str
#     published:bool
