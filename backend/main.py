from src.models.user import User
from fastapi import FastAPI, HTTPException, status, Depends
from src.models.user import User
from src.db.connection import chat_completion
from src.controller.user_controllers import (
    signup_user, get_user, login_user, create_token )
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

@app.post("/user/signup", response_model=User)
async def post_user_signup(user: User):
    response = await signup_user(user)
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong")

@app.post("/user/login")
async def post_user_login(user: User):
#async def create_token(
#    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)
#): 
#로그인 시 받아줄 폼을 OAuth2PasswordRequestForm를 사용, python-multipart 필요함
    #회원 존재하는지 확인
    user_exist = await get_user(user.id)
    if not user_exist:
        raise HTTPException(404, "User not found")
    #회원 존재하면 로그인
    res = await login_user(user.password, user_exist['password'])
    if not res:
        raise HTTPException(401, detail="wrong pswd")
    #토큰 생성-유효기간은 30분으로 설정함
    token = await create_token(user.id)
    return {"success":"login successful", "token": token}

@app.post("/chat/new", response_model=User)
async def post_new_chat(user_id: str, message: str):
    response = await chat_completion(user_id, message)
    if response:
        return response
    raise HTTPException(500, "Smth went wrong ;)")
