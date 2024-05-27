from src.models.user import User
from fastapi import FastAPI, HTTPException, Depends
from src.models.user import User
from src.db.connection import collection

from src.controller.chat_controller import (chat_completion_classroom, get_classroom_chat, get_class_concepts, get_concept_chat)
from src.controller.user_controllers import (signup_user, login_user, create_classroom, change_classroom_name, delete_classroom, delete_classroom_concept, get_all_classes)
from src.controller.concept_controller import (chat_completion_supplement, chat_completion_qna)
from src.controller.auth_controllers import (auth_get_current_user)

import os
from dotenv import load_dotenv
load_dotenv()
frontend_url = os.getenv("FRONTEND_URL")

# FastAPI의 CORS(Cross-Origin Resource Sharing)를 지원하는 미들웨어
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# React 연결
origins = [
    frontend_url,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE","OPTIONS"],
    allow_headers=["*"],
)

# Default
@app.get('/')
def index():
    return{"일구어냄 졸업 프로젝트: CATCHUP"}

## Chat 관리 BACKEND -------

# GET: 기본 챗방의 모든 Chat
# 해당 기본 챗방에서 모든 챗 기록들을 반환해줌
@app.get('/user/getallchats')
async def get_all_chats(classroom_id:str, user_id:dict = Depends(auth_get_current_user)):
    response = await get_classroom_chat(user_id["id"], classroom_id)
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong")

# GET: 기본 챗방의 개념 챗방 리스트
# 해당 기본 챗방에서 생성된 개념 챗방 리스트를 반환해줌
@app.get('/chat/getclassconcepts')
async def get_all_class_concepts(classroom_id:str, user_id:dict = Depends(auth_get_current_user)):
    response = await get_class_concepts(user_id["id"], classroom_id)
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong")
    
# GET: 개념 챗방의 모든 Chat
# 해당 개념 챗방에서 모든 챗 기록들을 반환해줌
@app.get('/getconceptchats')
async def get_all_concept_chats(concept_id:str, classroom_id:str, user_id:dict = Depends(auth_get_current_user)):
    response = await get_concept_chat(user_id["id"], classroom_id, concept_id)
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong")

# POST: 기본 챗방의 Chat_Completion
# 기본 챗방에서 사용자 입력에 따라 필요한 개념 챗방을 생성해주는 Chat Completion
@app.post("/chat/new/{classroom_id}/{message}", response_model=list)
async def post_new_chat(classroom_id:str, message: str, user_id:dict = Depends(auth_get_current_user)):
    response = await chat_completion_classroom(user_id["id"], message, classroom_id)
    if response:
        return response
    raise HTTPException(400, "Smth went wrong ;)")

# POST: 개념 챗방의 Chat_Completion
# 개념 챗방에서 해당 개념과 관련된 학습 자료를 생성해주는 Chat Completion
@app.post("/chat/concept/supplement/{classroom_id}/{concept_id}", response_model=list)
async def post_new_concept_supplement(classroom_id:str, concept_id:str, user_id:dict = Depends(auth_get_current_user)):
    response = await chat_completion_supplement(user_id["id"], classroom_id, concept_id)
    if response:
        return response
    raise HTTPException(500, "Smth went wrong ;)")

# POST: Q&A Chat_Completion
# 개념 챗방에서 학습 자료를 바탕으로 사용자 질문에 답을 해주는 Chat Completion
@app.post("/chat/concept/qna/{classroom_id}/{message}/{concept_id}", response_model=list)
async def post_new_concept_qna(classroom_id:str, message: str, concept_id:str, user_id:dict = Depends(auth_get_current_user)):
    response = await chat_completion_qna(user_id["id"], message, classroom_id, concept_id)
    if response:
        return response
    raise HTTPException(500, "Smth went wrong ;)")

## --------

## 사용자 관리 BACKEND ----

# POST: 회원가입
@app.post("/user/signup", response_model=User)
async def post_user_signup(user: User):
    response = await signup_user(user)
    if response:
        return response
    else:
        raise HTTPException(400, "Something went wrong!")

# POST: 로그인
@app.post("/user/login")
async def post_user_login(user: User):
        response = await login_user(user)
        if response:
            return response
        else:
            raise HTTPException(400, "Something went wrong!")
        
## --------

## Dashboard 관리 BACKEND ----

# GET: 사용자의 모든 기본 챗방 리스트
# 해당 사용자의 모든 기본 챗방 리스트를 반환해줌
@app.get("/user/dashboard")
async def get_classroomList(user_id: dict = Depends(auth_get_current_user)):
    response = await get_all_classes(user_id["id"])
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")

# POST: ClassroomName 수정
# 해당 사용자의 Classroom 속의 classroomid에 해당하는 classroomName을 수정함
@app.post("/user/clsm/change/{classroom_id}/{new_classroom_name}")
async def post_change_classroom_name(classroom_id:str, new_classroom_name:str, user_id:dict = Depends(auth_get_current_user)):
    response = await change_classroom_name(classroom_id, new_classroom_name, user_id["id"])
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")
    
# POST: Classroom 삭제
# 해당 사용자의 Classroom 속의 classroomid에 해당하는 classroom을 삭제함
@app.post("/user/clsm/delete/{classroom_id}")
async def post_delete_classroom(classroom_id:str, user_id:dict = Depends(auth_get_current_user)):

    response = await delete_classroom(classroom_id, user_id["id"])
    if response:
        return response
    raise HTTPException(500, "Smth went wrong ;)")

# POST: 개념챗방 삭제
# 해당 사용자의 Classroom 속의 classroomid에 해당하는 classroom 속의 해당 개념 챗방을 삭제함
@app.post("/user/clsm/concept/delete/{classroom_id}/{concept_id}")
async def post_delete_classroom_concept(classroom_id:str, concept_id:str, user_id:dict = Depends(auth_get_current_user)):
    response = await delete_classroom_concept(classroom_id, concept_id, user_id["id"])
    if response:
        return response
    raise HTTPException(500, "Smth went wrong ;)")


# POST: 기본 챗방 생성
# 새로운 기본 챗방을 생성함
@app.post("/user/classroom/new")
async def post_create_classroom(user_id: dict = Depends(auth_get_current_user)):
    response = await create_classroom(user_id["id"])
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")

## --------



# 랭체인 테스트 -- 나중에 삭제예정
from src.controller.langchain_controllers import (langchain_conceptlist, langchain_learningmaterial, langchain_qna)
@app.post("/test/answer0")
async def langchain_check0(flag: int, course: str):
    response = await langchain_conceptlist(flag, course)
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")

@app.post("/test/answer1")
async def langchain_check1(flag: int, concept: str):
    response = await langchain_learningmaterial(flag, concept)
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")

@app.post("/test/answer2")
async def langchain_check2(flag: int, question: str, chat: str):
    response = await langchain_qna(flag, question, chat)
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")