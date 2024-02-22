#테스트용 (mina)
from fastapi import HTTPException
from ..db.connection import collection
#from passlib.hash import bcrypt
import bcrypt

#로그인 테스트 위해 비밀번호 암호화 구현
async def create_user_test(user):
    #암호화 부분 for ej
#    hashed_password_ej = bcrypt.hash(user.password)
#    document = {"name": user.name, "email": user.email, "id": user.id, "password": hashed_password_ej}
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    document = {"name": user.name, "email": user.email, "id": user.id, "password": hashed_password.decode('utf-8')}
    result = await collection.insert_one(document)
    #await collection.insert_one(document) 이렇게 썼을 때의 차이가 있을까
    #collection.insert_one(document) 이렇게 쓰면 동기라는데 괜찮나
    return document

#해당 id의 회원이 존재하는지 확인, 존재하면 해당 id를 가지는 객체 하나를 반환
async def get_user(id):
    document = await collection.find_one({"id":id})
    return document

#입력받은 비밀번호를 해당 id에 저장된 암호화된 비밀번호와 비교함
async def login_user(entered_password, exist_password):
    pw_entered = entered_password.encode('utf-8')
    pw_stored = exist_password.encode('utf-8')
#    ps_match = bcrypt.verify(pw_entered, pw_stored)
    ps_match = bcrypt.checkpw(pw_entered, pw_stored)
    return ps_match

