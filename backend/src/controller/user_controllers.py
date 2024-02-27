import uuid
from fastapi import HTTPException, Request
import bcrypt
from src.models.user import Chat, Classroom, User
from ..db.connection import collection
import datetime
import jwt

async def signup_user(user):
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(400, "User already existed!")
    existing_id = await collection.find_one({"id":user.id})
    if existing_id:
        raise HTTPException(400, "This Id is already used!")
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    document = {"name": user.name, "email": user.email, "id": user.id, "password": hashed_password.decode('utf-8')}
    collection.insert_one(document)
    return document

#해당 id의 회원이 존재하는지 확인, 존재하면 해당 id를 가지는 객체 하나를 반환
async def get_user(id):
    document = await collection.find_one({"id":id})
    return document

#입력받은 비밀번호를 해당 id에 저장된 암호화된 비밀번호와 비교함
async def login_user(entered_password, exist_password):
    pw_entered = entered_password.encode('utf-8')
    pw_stored = exist_password.encode('utf-8')
    ps_match = bcrypt.checkpw(pw_entered, pw_stored)
    return ps_match

#토큰 생성-유효기간은 1일로 설정함, secret 부분은 이후 환경변수 사용
async def create_token(id):
    payload = {"id":id,
               "exp": datetime.datetime.now()+datetime.timedelta(days=1)}
    token = jwt.encode(payload, "secret", algorithm="HS256")
    return token

# #토큰 유효성 검사_유효한 토큰인지 확인하고 사용자 반환
# async def get_current_user(request: Request):
#     return 0
# #사용자별로 DB에서 프론트로 데이터 전송 테스트용
# async def user_test():
#     return 0

# 강의실 생성
async def create_classroom(user_id, msg: str):
    # 새로 생성한 클래스룸 ID
    new_classroom_id = str(uuid.uuid4())
    # 사용자를 데이터베이스에서 찾기
    user = await collection.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # 사용자 객체가 딕셔너리가 아닌 User 모델의 인스턴스인지 확인
    if isinstance(user, dict):
        user = User(**user)
    # 새로운 클래스룸 생성
    new_classroom = Classroom(classroomId=new_classroom_id, classroomName="First Classroom", conceptList=[], chatList=[Chat(content=msg, role="user")])
    # 사용자의 클래스룸 리스트에 새로운 클래스룸 추가
    if not user.classroomList:
        user.classroomList = [new_classroom]
    else:
        user.classroomList.append(new_classroom)
    # 사용자 업데이트
    await collection.update_one(
        {"id": user_id},
        {"$set": {"classroomList": [classroom.dict() for classroom in user.classroomList]}}
    )
    return new_classroom_id