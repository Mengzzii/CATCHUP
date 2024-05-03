from fastapi import HTTPException
from pydantic import BaseModel, validator, EmailStr
from typing import List
import uuid

# 챗의 data model
class Chat(BaseModel):
    id: str = str(uuid.uuid4())
    role: str
    content: str

# 개념 챗방의 data model
class Concept(BaseModel):
    name: str
    conceptId: str = str(uuid.uuid4())
    chatList: List[Chat]

# 기본 챗방의 data model
class Classroom(BaseModel):
    classroomName: str
    classroomId: str = str(uuid.uuid4())
    conceptList: List[Concept]
    chatList: List[Chat]

# 사용자의 data model
class User(BaseModel):
    name: str
    email: EmailStr
    id: str
    password: str
    # 필수 입력 값에서 제외
    classroomList: List[Classroom] | None = None
    
    # 비밀번호 생성 규칙
    # 8자리 이상 숫자와 알파벳
    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise HTTPException(422, "Need 8 characters at least!")
        if not any(char.isdigit() for char in v):
            raise HTTPException(422, "Need number!")
        if not any(char.isalpha() for char in v):
            raise HTTPException(422, "Need alphabet!")
        return v