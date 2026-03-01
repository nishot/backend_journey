from sqlalchemy import Column, Integer, String,Boolean,DateTime,func,ForeignKey
from .database import Base
from sqlalchemy.dialects.mysql import VARBINARY
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__="posts"

    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String(255),nullable=False)
    content=Column(String(255),nullable=False)
    published=Column(Boolean,default='True',nullable=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    user=relationship("User")

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email= Column(String(255),nullable=False,unique=True)
    password=Column(String(255),nullable=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    phone_number =Column(String)
    


class Vote(Base):
    __tablename__="vote"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True) 