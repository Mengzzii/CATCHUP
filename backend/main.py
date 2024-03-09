from typing import Dict, List
from src.models.user import User
from fastapi import FastAPI, HTTPException, status, Depends, Header
from src.models.user import User
from src.db.connection import collection
from src.controller.chat_controller import (chat_completion, get_sample_chat, get_class_concepts)
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

@app.get('/sample/getallchats/{id}/{classroom_id}')
async def get_sample_all_chats(id:str,classroom_id:str):
    response = await get_sample_chat(id, classroom_id)
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong")
    

@app.get('/getclassconcepts/{id}/{classroom_id}')
async def get_all_class_concepts(id:str,classroom_id:str):
    response = await get_class_concepts(id, classroom_id)
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

#토큰을 받아서 검사하고 id를 준다
from src.controller.user_controllers import get_current_user
@app.get("/user/auth_get_current_user/{token}")
async def auth_get_current_user(token):
    response = await get_current_user(token)
    if response:
        return {"id": response}
    raise HTTPException(401, "unauthorized user")

#토큰 이용한 연결테스트
#토큰을 받아서 검사하고 id를 준다
async def auth_get_current_user(tokens: str = Header(...)):
    response = await get_current_user(tokens)
    if response:
        return {"id": response}
    raise HTTPException(401, "unauthorized user")
@app.post("/user/test/classroom/new")
async def test_post_create_classroom(user_id: dict = Depends(auth_get_current_user)):
    response = await create_classroom(user_id["id"])
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")
#토큰 이용한 연결테스트

@app.post("/chat/new/{user_id}/{classroom_id}/{message}", response_model=list)
async def post_new_chat(user_id: str, message: str, classroom_id:str):
    response = await chat_completion(user_id, message, classroom_id)
    if response:
        return response
    raise HTTPException(500, "Smth went wrong ;)")

@app.post("/user/classroom/new/{user_id}")
async def post_create_classroom(user_id: str):
    response = await create_classroom(user_id)
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")

@app.post("/user/classroom/store-concepts/{user_id}/{classroom_id}")
async def post_store_concepts(user_id: str, classroom_id: str):
    response= await store_concept(user_id, classroom_id)
    if response:
        return {"message": "Concepts stored successfully"}
    raise HTTPException(400, "Something went wrong!")