from fastapi import FastAPI
# import mysql.connector
# import time 
from . import model ,database
from .routers import post ,user,auth,vote
from .config import setting
from fastapi.middleware.cors import CORSMiddleware


# model.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origin=[
    "https://www.google.com/",'*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message:  hello world " }
