from fastapi import HTTPException
import bcrypt
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

#토큰 생성-유효기간은 30분으로 설정함, secret 부분은 이후 환경변수 사용
async def create_token(id):
    payload = {"id":id,
               "exp": datetime.datetime.now()+datetime.timedelta(minutes=30)}
    token = jwt.encode(payload, "secret", algorithm="HS256")
    return token
