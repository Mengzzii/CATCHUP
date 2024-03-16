from fastapi import FastAPI, HTTPException, status, Depends, Header
from src.controller.user_controllers import (get_current_user)

async def auth_get_current_user(token: str = Header(...)):
    response = await get_current_user(token)
    if response:
        return {"id": response}
    raise HTTPException(401, "unauthorized user")