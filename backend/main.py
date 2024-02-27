from typing import Dict, List
from src.models.user import User
from fastapi import FastAPI, HTTPException, status, Depends
from src.models.user import User
from src.db.connection import collection
from src.controller.chat_controller import (chat_completion, get_sample_chat)
from src.controller.user_controllers import (
    signup_user, get_user, login_user, create_token, create_classroom )
from src.controller.conceptTest_controller import store_concept
# from fastapi.security import OAuth2PasswordRequestForm

# an HTTP-specific exception class  to generate exception information
#Cross Origin(Protocol, domain, port) Recource Share : 
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# React랑 연결
origins = [
    "http://localhost:5173",
]
# from src.controller.user_controllers import signup_user

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return{"name":"First Data"}

@app.get('/sample/getallchats/{id}')
async def get_sample_all_chats(id:str):
    response = await get_sample_chat(id)
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong")


@app.post("/user/signup", response_model=User)
async def post_user_signup(user: User):
    response = await signup_user(user)
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong!")

@app.post("/user/login")
async def post_user_login(user: User):
    #회원 존재하는지 확인
    user_exist = await get_user(user.id)
    if not user_exist:
        raise HTTPException(404, "User not found")
    #회원 존재하면 로그인
    res = await login_user(user.password, user_exist['password'])
    name = user_exist['name']
    if not res:
        raise HTTPException(401, detail="wrong pswd")
    #토큰 생성-유효기간은 1일
    token = await create_token(user.id)
    return {"success":"login successful", "token": token, "name": name}

# #사용자별로 DB에서 프론트로 데이터 전송 테스트용
# from src.controller.user_controllers import user_test 
# @app.get("/user/test")
# async def get_user_test():
#     response = await user_test(user)
#     if response:
#         return response
#     else:
#         raise HTTPException(400, "Something went wrong!")
# #사용자별로 DB에서 프론트로 데이터 전송 테스트용


@app.post("/chat/new/{user_id}/{classroom_name}/{message}", response_model=User)
async def post_new_chat(user_id: str, message: str, classroom_name:str):
    response = await chat_completion(user_id, message, classroom_name)
    if response:
        return response
    raise HTTPException(500, "Smth went wrong ;)")

@app.post("/user/classroom/new/{user_id}")
async def post_create_classroom(user_id: str, msg: str):
    response = await create_classroom(user_id, msg)
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")

@app.post("/user/classroom/store-concepts/{user_id}/{classroom_id}")
async def post_store_concepts(user_id: str, classroom_id: str):
    response= await store_concept(user_id, classroom_id)
    if response:
        return {"message": "Concepts stored successfully"}
    raise HTTPException(400, "Something went wrong!")