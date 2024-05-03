from fastapi import HTTPException, Header
from src.controller.user_controllers import (get_current_user)

# 현재 사용자 인증 함수
async def auth_get_current_user(token: str = Header(...)):
    response = await get_current_user(token)
    if response:
        return {"id": response}
    raise HTTPException(401, "unauthorized user")