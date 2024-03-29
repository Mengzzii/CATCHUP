from typing import Dict, List
from src.models.user import User
from fastapi import FastAPI, HTTPException, status, Depends, Header
from src.models.user import User
from src.db.connection import collection

from src.controller.chat_controller import (chat_completion_concept_deprecated, chat_completion_concept, get_sample_chat, get_class_concepts, get_concept_chat, get_concept_list)
from src.controller.user_controllers import (signup_user, get_user, login_user, create_token, create_classroom, get_current_user)
from src.controller.concept_controller import ( chat_completion_classroom)
from src.controller.auth_controllers import (auth_get_current_user)

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
    allow_methods=["GET", "POST", "PUT", "DELETE","OPTIONS"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return{"name":"First Data"}

@app.get('/json/getconceptlist')
async def get_json_concept_list():
    response = await get_concept_list()
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong")

@app.get('/user/getallchats')
async def get_all_chats(classroom_id:str, user_id:dict = Depends(auth_get_current_user)):
    response = await get_sample_chat(user_id["id"], classroom_id)
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong")
    
@app.get('/chat/getclassconcepts')
async def get_all_class_concepts(classroom_id:str, user_id:dict = Depends(auth_get_current_user)):
    response = await get_class_concepts(user_id["id"], classroom_id)
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong")
    
@app.post("/chat/new/{classroom_id}/{message}", response_model=list)
async def post_new_chat(classroom_id:str, message: str, user_id:dict = Depends(auth_get_current_user)):
    response = await chat_completion_classroom(user_id["id"], message, classroom_id)
    if response:
        return response
    raise HTTPException(500, "Smth went wrong ;)")

#!!!!!!!!!!!!!!!!!!!!!!!
@app.post("/chat/concept/new/{classroom_id}/{message}/{concept_id}", response_model=list)
async def post_new_chat_concept(classroom_id:str, message: str, concept_id:str, user_id:dict = Depends(auth_get_current_user)):
    response = await chat_completion_concept(user_id["id"], message, classroom_id, concept_id)
    if response:
        return response
    raise HTTPException(500, "Smth went wrong ;)")
    
@app.get('/getconceptchats')
async def get_all_concept_chats(concept_id:str, classroom_id:str, user_id:dict = Depends(auth_get_current_user)):
    response = await get_concept_chat(user_id["id"], classroom_id, concept_id)
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

##Dashboard
#User가 가지고 있는 모든 Classroom의 classroomName과 classroomId를 반환한다.
async def get_all_classes(user_id: str):
    user = await collection.find_one({"id":user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    class_name_id_List={}
    for classroom in user["classroomList"]:
        classId = classroom["classroomId"]
        className = classroom["classroomName"]
        class_name_id_List[classId] = className
    return class_name_id_List
@app.get("/user/dashboard")
async def get_classroomList(user_id: dict = Depends(auth_get_current_user)):
    response = await get_all_classes(user_id["id"])
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")

#User의 Classroom 속의 classroomid에 해당하는 classroomName을 수정한다.
async def change_classroom_name(user_id: str, classroom_id: str):
    user = await collection.find_one({"id":user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    classroom = None
    for clsrm in user["classroomList"]:
        if clsrm["classroomId"] == classroom_id:
            classroom = clsrm
            break
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
##Dashboard

@app.post("/user/classroom/new")
async def post_create_classroom(user_id: dict = Depends(auth_get_current_user)):
    response = await create_classroom(user_id["id"])
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")

@app.post("/user/chat/check/store/combine/{user_id}/{classroom_id}")
async def post_chat_check_store(user_id:str, classroom_id:str, msg):
    response = await chat_completion_classroom(user_id, classroom_id, msg)
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")

@app.post("/test/{classroom_id}/{message}/{concept_id}/{user_id}")
async def post_new_chat_concept(classroom_id:str, message: str, concept_id:str, user_id:str):
    response = await chat_completion_concept_deprecated(user_id, message, classroom_id, concept_id)
    if response:
        return response
    raise HTTPException(500, "Smth went wrong ;)")