from fastapi import HTTPException
from passlib.hash import bcrypt
from ..db.connection import collection

async def signup_user(user):
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(400, "User already existed!")
    existing_id = await collection.find_one({"id":user.id})
    if existing_id:
        raise HTTPException(400, "This Id is already used!")
    hashed_password = bcrypt.hash(user.password)
    document = {"name": user.name, "email": user.email, "id": user.id, "password": hashed_password}
    collection.insert_one(document)
    return document
