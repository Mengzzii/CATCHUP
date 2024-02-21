from src.models.user import User
from fastapi import FastAPI, HTTPException, status, Depends
from src.models.user import User
from src.db.connection import (
    create_user,
    chat_completion
)
#민아
#from src.controller.user_controllers import ()
from fastapi.security import OAuth2PasswordRequestForm
from src.controller.test import (create_user_test, get_user, login_user)
from src.controller.user_controllers import signup_user
#민아

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
    allow_origins=["http://localhost:5173"],
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

#민아 여기부터
@app.post("/user", response_model=User)
async def post_user_test(user: User):
    #response = await create_user(user.model_dump()) 로는 오류떠서 바꿈
    response = await create_user_test(user)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")
    
@app.post("/user/login")
async def post_user_login(user: User):
#async def create_token(
#    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)
#):
    #회원 존재하는지 확인
    user_exist = await get_user(user.id)
    if not user_exist:
        raise HTTPException(404, "User not found")
    #회원 존재하면 로그인
    res = await login_user(user.password, user_exist['password'])
    if not res:
        raise HTTPException(401, detail="wrong pswd")
    return {"msg":"login successful"}
#민아 여기까지

@app.post("/chat/new", response_model=User)
async def post_new_chat(user_id: str, message:str):
    response = await chat_completion(user_id, message)
    if response:
        return response
    raise HTTPException(500, "Smth went wrong ;)")
