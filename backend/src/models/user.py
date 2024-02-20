from pydantic import BaseModel, Field
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
