from fastapi import HTTPException
from pydantic import BaseModel, validator, EmailStr
from typing import List
import uuid

class Chat(BaseModel):
    id: str = str(uuid.uuid4())
    role: str
    content: str

class Concept(BaseModel):
    name: str
    conceptId: str = str(uuid.uuid4())
    chatList: List[Chat]

class Classroom(BaseModel):
    classroomName: str
    classroomId: str = str(uuid.uuid4())
    conceptList: List[Concept]
    chatList: List[Chat]

class User(BaseModel):
    name: str
    email: EmailStr
    id: str
    password: str
    # 필수 입력 값에서 제외
    classroomList: List[Classroom] | None = None
    
    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise HTTPException(422, "Need 8 characters at least!")
        if not any(char.isdigit() for char in v):
            raise HTTPException(422, "Need number!")
        if not any(char.isalpha() for char in v):
            raise HTTPException(422, "Need alphabet!")
        return v
    
class User_test(BaseModel):
    name: str
    email: str
    id: str
    password: str
    # 필수 입력 값에서 제외
    classroomList: List[Chat] | None = None