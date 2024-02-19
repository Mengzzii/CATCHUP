from fastapi import FastAPI, HTTPException
from src.models.user import User, usersignup
from src.db.connection import (
    create_user
)
from src.controller.user_controllers import signup_user

# an HTTP-specific exception class  to generate exception information
#Cross Origin(Protocol, domain, port) Recource Share : 
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# React랑 연결
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return{"name":"First Data"}


@app.post("/user", response_model=User)
async def post_user(user: User):
    response = await create_user(user.model_dump())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")


@app.post("/user/signup", response_model=usersignup)
async def post_user_signup(user: usersignup):
    response = await signup_user(user)
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong")
    

@app.post("/user/login", response_model=User)
async def post_user_signup(user: User):
    return 1

@app.post("/chat/new", response_model=User)
async def post_new_chat(user: User):
    return 1
##