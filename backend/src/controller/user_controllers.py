from fastapi import HTTPException
import motor.motor_asyncio
from passlib.hash import bcrypt
from ..models.user import User

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
# database = client.Check
# collection = database.new

# async def signup_user(user):
#     try:    # 이메일 중복 확인
#         #existing_user = await collection.find_one({"email": user.email})
#         #if existing_user:
#         #    raise HTTPException(400, "User already existed!")
#         # 비밀번호 해싱
#         # hashed_password = await bcrypt.hash(user.password)
#         # # # 새로운 사용자 생성
#         # document = {"name": user.name, "email": user.email, "id": user.id, "password": hashed_password}
#         document = user
#         # result = await collection.insert_one(document)
#         # 성공적으로 등록된 사용자 정보 반환
#         return document
#     except Exception as e:
#         # 예외 처리: 회원가입 실패
#         raise HTTPException(500, "Failed to register user...")
  
# async def create_user(user):
#     document = user
#     result = await collection.insert_one(document)
#     return document