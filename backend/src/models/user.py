from fastapi import HTTPException
from pydantic import BaseModel, validator, EmailStr
from typing import List, Optional
import uuid

class Chat(BaseModel):
    id: str = str(uuid.uuid4())
    role: str
    content: str

class User(BaseModel):
    name: str
    email: str
    id: str
    password: str
    chats: Optional[List[Chat]] = []

    # class Config:
    #     orm_mode = True

class Chatroom(BaseModel):
    userId: str
    chatId: str = str(uuid.uuid4())
    chats: List[Chat]

class usersignup(BaseModel):
    name: str
    email: EmailStr
    id: str
    password: str
    # 필수 입력 값에서 제외
    chatroomList: List[Chatroom] | None = None
    
    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise HTTPException(422, "Need 8 characters at least!")
        if not any(char.isdigit() for char in v):
            raise HTTPException(422, "Need number!")
        if not any(char.isalpha() for char in v):
            raise HTTPException(422, "Need alphabet!")
        return v