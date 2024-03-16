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
    print(id)
    print(classroom_id)
    user = await collection.find_one({"id":id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    target_classroom = None
    
    #find classroom
    for classroom in user["classroomList"]:
        if classroom["classroomId"]==classroom_id:
            target_classroom = classroom
            print(target_classroom)
            break
    
    if target_classroom == None:
        raise HTTPException(status_code=404, detail=f"Classroom ID '{classroom_id}' not found")
    
    chats_to_send = [{"role": chat["role"], "content": chat["content"]} for chat in target_classroom["chatList"]]
    print(chats_to_send)
    return chats_to_send

async def get_concept_chat(id:str, classroom_id:str, concept_id:str):
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
    
    target_concept = None

    #find concept
    for concept in target_classroom["conceptList"]:
        if concept["conceptId"]==concept_id:
            target_concept = concept
            break
    
    if target_concept == None:
        raise HTTPException(status_code=404, detail=f"Concept ID '{concept_id}' not found")
    
    chats_to_send = [{"role": chat["role"], "content": chat["content"]} for chat in target_concept["chatList"]]
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

async def get_concept_list():
    course_name = 'Computer Algorithm'
    client = openai_config()
    json_response = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[
    {
      "role": "user",
      "content": f'''You are a Professor of a '{course_name}' course. Please generate a list of essential prerequisites of this course in  specific mathematical concepts, narrowed enough to be covered within 40 minutes. \n\nGuidelines to formatting:\n- Each concepts should be presented as a value in a JSON form. The key should be 'name'. \n- No  code block delimiter. No '\\n' or backslash('\') in output. \n- example :  [{{"name": "concept1"}}, {{"name": "concept2"}}, {{"name": "concept3"}}]'''
    }
  ],
  temperature=0.2,
  max_tokens=564,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
    print('!!!!!!!!!!!!!!!!!!')
    print(json_response.choices[0].message.content)
    return json_response.choices[0].message.content




