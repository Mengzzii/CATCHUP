import uuid
from fastapi import HTTPException, Request
import bcrypt
from src.models.user import Classroom, User
from ..db.connection import collection
import datetime
import jwt

# 회원가입
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

# 해당 id의 회원이 존재하는지 확인, 존재하면 해당 id를 가지는 객체 하나를 반환
async def get_user(id):
    document = await collection.find_one({"id":id})
    return document

# 입력받은 비밀번호를 해당 id에 저장된 암호화된 비밀번호와 비교함
async def checkps_user(entered_password, exist_password):
    pw_entered = entered_password.encode('utf-8')
    pw_stored = exist_password.encode('utf-8')
    ps_match = bcrypt.checkpw(pw_entered, pw_stored)
    return ps_match

# SECRET_KEY, ALGORITHM, TOKEN_EXPIRETIME 등으로 이후 환경변수 사용 권장
# 토큰 생성-유효기간은 1일로 설정함
async def create_token(id):
    payload = {"id":id,
               "exp": datetime.datetime.utcnow()+datetime.timedelta(days=1)}
    secret_key = "mina0104"
    algorithm = "HS256"
    token = jwt.encode(payload, secret_key, algorithm)
    return token

# 토큰 유효성 검사_토큰을 받아서 유효한지 확인하고 해당 사용자id를 반환한다
async def get_current_user(token):
    secret_key = "mina0104"
    algorithm = "HS256"
    try:
        decoded_token = jwt.decode(token, secret_key, algorithm)
    except:
        raise HTTPException(401,"invalid token")
    userId = await get_user(decoded_token.get("id"))
    if not userId:
        raise HTTPException(401, "userID not found")
    return userId['id']

#로그인
async def login_user(user):
    #회원 존재하는지 확인
    user_exist = await get_user(user.id)
    if not user_exist:
        raise HTTPException(404, "User not found")
    #회원 존재하면 로그인
    res = await checkps_user(user.password, user_exist['password'])
    name = user_exist['name']
    if not res:
        raise HTTPException(401, detail="wrong pswd")
    #토큰 생성-유효기간은 1일
    token = await create_token(user.id)
    return {"success":"login successful", "token": token, "name": name}

# 강의실 생성
async def create_classroom(user_id):
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
    new_classroom = Classroom(classroomId=new_classroom_id, classroomName="Empty Classroom", conceptList=[], chatList=[])
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

## Dashboard 관리 BACKEND ----

# User가 가지고 있는 모든 Classroom의 classroomName과 classroomId를 반환한다.
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

# POST: ClassroomName 수정
# 해당 사용자의 Classroom 속의 classroomid에 해당하는 classroomName을 수정함
async def change_classroom_name(classroom_id:str, new_classroom_name:str, user_id:str):
    user = await collection.find_one({"id":user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await collection.update_one(
        {"id": user_id, "classroomList.classroomId": classroom_id},
        {"$set": {"classroomList.$.classroomName": new_classroom_name}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Classroom not found or name not updated")

    return {"detail": "Classroom name updated successfully"}
    
    
# POST: Classroom 삭제
# 해당 사용자의 Classroom 속의 classroomid에 해당하는 classroom을 삭제함
async def delete_classroom(classroom_id:str, user_id:str):
    user = await collection.find_one({"id":user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await collection.update_one(
        {"id": user_id},
        {"$pull": {"classroomList": {"classroomId": classroom_id}}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Classroom not found")

    return {"detail": "Classroom deleted successfully"}

# POST: 개념챗방 삭제
# 해당 사용자의 Classroom 속의 classroomid에 해당하는 classroom 속의 해당 개념 챗방을 삭제함
async def delete_classroom_concept(classroom_id:str, concept_id:str, user_id:str):
    user = await collection.find_one({"id":user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await collection.update_one(
        {"id": user_id,"classroomList.classroomId":classroom_id},
        {"$pull": {"classroomList.$.conceptList": {"conceptId": concept_id}}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Classroom not found")

    return {"detail": "Classroom deleted successfully"}