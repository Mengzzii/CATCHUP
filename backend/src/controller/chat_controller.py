from openai import OpenAI
from dotenv import load_dotenv
import os
from ..db.connection import collection
from fastapi import HTTPException
from bson.objectid import ObjectId
import uuid

load_dotenv()

# async def update_todo(title, desc):
#     await collection.update_one({"title": title}, {"$set": {"description": desc}})
#     document = await collection.find_one({"title": title})
#     return document

def openai_config():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    return client


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

async def get_sample_chat(id:str):
    user = await collection.find_one({"id":id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    chats_to_send = [{"role": chat["role"], "content": chat["content"]} for chat in user["classroomList"][0]["chatList"]]
    return chats_to_send




