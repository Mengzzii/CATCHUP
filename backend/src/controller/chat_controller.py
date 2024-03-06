from ..db.connection import collection
from fastapi import HTTPException
from bson.objectid import ObjectId
import uuid
from ..config.openai_config import openai_config
from ..models.user import Classroom


async def chat_completion(user_id: str, msg, classroom_id):
    # Retrieve the user from the database
    user = await collection.find_one({"id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find the classroom by name
    target_classroom = None
    for classroom in user["classroomList"]:
        if classroom["classroomId"] == classroom_id:
            target_classroom = classroom
            break

    if target_classroom is None:
        raise HTTPException(status_code=404, detail=f"Classroom '{classroom_id}' not found")

    # Access the chatList from the target classroom
    chat_list = target_classroom["chatList"]

    # grab chats of user to send
    chats_to_send = [{"role": chat["role"], "content": chat["content"]} for chat in chat_list]
    chats_to_send.append({"content": msg, "role": "user"})

    # Update the user in the database with the new chat
    new_chat = {"id": str(uuid.uuid4()),"content": msg, "role": "user"}
    target_classroom["chatList"].append(new_chat)
    #user["chats"].append(new_chat)

    # send all chats with new one to openAI API
    client = openai_config()

    # get latest response
    chat_response = client.chat.completions.create( model="gpt-3.5-turbo", messages=chats_to_send)
    new_res = {"id": str(uuid.uuid4()),"content": chat_response.choices[0].message.content, "role": "assistant"}
    #user["chats"].append(new_res)
    target_classroom["chatList"].append(new_res)

    # Update the user's classroomList with the modified list
    updated_classroom_list = [c for c in user["classroomList"] if c['classroomId'] != classroom_id]  # Remove existing classroom
    updated_classroom_list.append(target_classroom)

    user["classroomList"] = updated_classroom_list

    result = await collection.update_one(
        {"id": user_id}, {"$set": user}
    )
    return target_classroom["chatList"]

async def get_sample_chat(id:str, classroom_id:str):
    user = await collection.find_one({"id":id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    target_classroom = None
    
    #find classroom
    for classroom in user["classroomList"]:
        if classroom["classroomId"]==classroom_id:
            target_classroom = classroom
            break
    
    if target_classroom == None:
        raise HTTPException(status_code=404, detail=f"Classroom ID '{classroom_id}' not found")
    
    chats_to_send = [{"role": chat["role"], "content": chat["content"]} for chat in target_classroom["chatList"]]
    return chats_to_send

async def get_class_concepts(id:str, classroom_id:str):
    user = await collection.find_one({"id":id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    #find classroom
    for classroom in user["classroomList"]:
        if classroom["classroomId"]==classroom_id:
            target_classroom = classroom
            break
    
    if target_classroom == None:
        raise HTTPException(status_code=404, detail=f"Classroom ID '{classroom_id}' not found")
    
    concept_name_list = []
    for concept in target_classroom["conceptList"]:
        concept_name_list.append(concept["name"])
    
    return concept_name_list
    




