

from fastapi import FastAPI, HTTPException

from src.models.user import User
from src.db.connection import (
    create_user
)

# from database import (
#     fetch_one_todo,
#     fetch_all_todos,
#     create_todo,
#     update_todo,
#     remove_todo,
# )

# an HTTP-specific exception class  to generate exception information
#Cross Origin(Protocol, domain, port) Recource Share : 
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# React랑 연결
origins = [
    "http://localhost:3000",
]


@app.post("/user", response_model=User)
async def post_user(user: User):
    response = await create_user(user.model_dump())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

##
@app.post("/user/signup", response_model=User)
async def post_user_signup(user: User):
    return 1

@app.post("/user/login", response_model=User)
async def post_user_signup(user: User):
    return 1

@app.post("/chat/new", response_model=User)
async def post_new_chat(user: User):
    return 1