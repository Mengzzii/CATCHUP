from fastapi import HTTPException
from bson.objectid import ObjectId
# MongoDB driver
import motor.motor_asyncio
from ..models.user import User
from ..controller.chat_controller import (openai_config)
import uuid

password = 'veGyue6hfhqurykH'
MONGO_URL = f"mongodb+srv://estherliu919:{password}@cluster0.dy560h4.mongodb.net/"

#이 파일과 mongoDB 연결
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.Test

# SQL table이랑 같은 개념
collection = database.users

async def create_user(user):
    document = user
    result = await collection.insert_one(document)
    return document

async def chat_completion(user_id: str, msg):
    # Retrieve the user from the database
    user = await collection.find_one({"id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # grab chats of user to send
    chats_to_send = [{"role": chat["role"], "content": chat["content"]} for chat in user["chats"]]
    chats_to_send.append({"content": msg, "role": "user"})

    # Update the user in the database with the new chat
    new_chat = {"id": str(uuid.uuid4()),"content": msg, "role": "user"}
    user["chats"].append(new_chat)

    # send all chats with new one to openAI API
    client = openai_config()

    # get latest response
    chat_response = client.chat.completions.create( model="gpt-3.5-turbo", messages=chats_to_send)
    new_res = {"id": str(uuid.uuid4()),"content": chat_response.choices[0].message.content, "role": "assistant"}
    user["chats"].append(new_res)
    result = await collection.update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": {"chats": user["chats"]}}
    )
    return user