from ..db.connection import collection
from fastapi import HTTPException
from bson.objectid import ObjectId
import uuid
from ..config.openai_config import openai_config
from .langchain_controllers import (langchain_conceptlist)
from ..models.user import Classroom
import json

#개념 챗방에서의 챗
async def chat_completion_concept(user_id: str, msg, classroom_id, concept_id):
    pipeline = [
        {"$unwind": "$classroomList"},  # Unwind the classroomList array
        {"$match": {"classroomList.classroomId": classroom_id}},  # Match documents with the given ID
        {"$unwind": "$classroomList.conceptList"},  # Unwind the conceptList array
        {"$match": {"classroomList.conceptList.conceptId": concept_id}},
        {"$replaceRoot": {"newRoot": "$classroomList.conceptList"}},  # Replace root with the inner_structure
        {"$project": { "name": 0, "conceptId": 0, "chatList": {"id": 0 }}}
    ]
    
    result = await collection.aggregate(pipeline).to_list(None)
    
    if not result:
        raise HTTPException(status_code=404, detail="Inner structure not found")

    # Send all chats with new one to openAI API
    chats_to_send = result[0]["chatList"]
    chats_to_send.append({"content": msg, "role": "user"})

    client = openai_config()
    res = client.chat.completions.create( model="gpt-3.5-turbo", messages=chats_to_send).choices[0].message.content
    chats_to_send.append({"content": res, "role": "assistant"})

    # # Update DB by appending msg & res
    # ## 1. format (give ID/role) to each chat
    db_res = {"id": str(uuid.uuid4()),"content": res, "role": "assistant"}
    db_msg = {"id": str(uuid.uuid4()),"content": msg, "role": "user"}
    ## 2. update
    updated_user = await collection.update_one(
        {"classroomList.classroomId": classroom_id},
        {"$push": {"classroomList.$.conceptList.$[concept].chatList": {"$each":[db_msg,db_res]}}},
        array_filters=[{"concept.conceptId": concept_id}]
    )

    if updated_user.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    # Return Updated Chatlist
    return chats_to_send



async def chat_completion_classroom(user_id: str, msg, classroom_id):
    pipeline = [
        {"$unwind": "$classroomList"},  # Unwind the classroomList array
        {"$match": {"classroomList.classroomId": classroom_id}},  # Match documents with the given ID
        {"$replaceRoot": {"newRoot": "$classroomList"}},  # Replace root with the inner_structure
        {"$project": {"classroomName":0, "classroomId":0,"conceptList":0, "chatList": { "id": 0}}}
    ]
    
    result = await collection.aggregate(pipeline).to_list(None)
    
    if not result:
        raise HTTPException(status_code=404, detail="Inner structure not found")

    chats_to_send = result[0]["chatList"]
    chats_to_send.append({"content": msg, "role": "user"})

    res = await langchain_conceptlist(0, msg)
    
    try:
        parsed_msg = json.loads(res)
        print(parsed_msg)
        # If parsing is successful, treat msg as JSON
        print(parsed_msg)
        concept_list = [{"name": concept["name"], "conceptId": str(uuid.uuid4()), "chatList": []} for concept in parsed_msg]

        updated_user = await collection.update_one(
        {"classroomList.classroomId": classroom_id},
        {"$push": {"classroomList.$.conceptList": {"$each":concept_list}, "classroomList.$.chatList": {"id": str(uuid.uuid4()), "role": "user","content": msg}}}
    )   

        if updated_user.matched_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")

    except json.JSONDecodeError:
        db_msg = {"id": str(uuid.uuid4()), "role": "user","content": msg}
        db_res = {"id": str(uuid.uuid4()),"role": "assistant", "content": res}

        updated_user = await collection.update_one(
        {"classroomList.classroomId": classroom_id},
        {"$push": {"classroomList.$.chatList": {"$each":[db_msg,db_res]}}}
    )
        if updated_user.matched_count == 0:
            raise HTTPException(status_code=404, detail="Chat Item not found")

    # Return Updated Chatlist
    return chats_to_send




## 옛날꺼라 나중에 버리기------------------------------------------------------------------
async def chat_completion_concept_deprecated(user_id: str, msg, classroom_id, concept_id):
    # Retrieve the user from the database
    user = await collection.find_one({"id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find the classroom by id
    target_classroom = None
    for classroom in user["classroomList"]:
        if classroom["classroomId"] == classroom_id:
            target_classroom = classroom
            break

    if target_classroom is None:
        raise HTTPException(status_code=404, detail=f"Classroom '{classroom_id}' not found")
    
    # Find concept by id
    target_concept = None
    for concept in target_classroom["conceptList"]:
        if concept["conceptId"] == concept_id:
            target_concept = concept
            break

    if target_concept is None:
        raise HTTPException(status_code=404, detail=f"Classroom '{classroom_id}' not found")

    # Access the chatList from the target classroom
    chat_list = target_concept["chatList"]

    # grab chats of user to send
    chats_to_send = [{"role": chat["role"], "content": chat["content"]} for chat in chat_list]
    chats_to_send.append({"content": msg, "role": "user"})

    # Update the user in the database with the new chat
    new_chat = {"id": str(uuid.uuid4()),"content": msg, "role": "user"}
    target_concept["chatList"].append(new_chat)
    #user["chats"].append(new_chat)

    # send all chats with new one to openAI API
    client = openai_config()

    # get latest response
    chat_response = client.chat.completions.create( model="gpt-3.5-turbo", messages=chats_to_send)
    new_res = {"id": str(uuid.uuid4()),"content": chat_response.choices[0].message.content, "role": "assistant"}
    #user["chats"].append(new_res)
    target_concept["chatList"].append(new_res)

    # Update the user's classroomList with the modified list
    updated_classroom_list = [classroom for classroom in user["classroomList"] if classroom['classroomId'] != classroom_id]  # Remove existing classroom

    # Update the user's classroomList with the modified list
    updated_concept_list = [concept for concept in target_classroom["conceptList"] if concept['conceptId'] != concept_id]  # Remove existing concept
    updated_concept_list.append(target_concept)
    target_classroom["conceptList"] = updated_concept_list
    updated_classroom_list.append(target_classroom)

    user["classroomList"] = updated_classroom_list

    result = await collection.update_one(
        {"id": user_id}, {"$set": user}
    )
    return target_concept["chatList"]

#옛날버전 : 기본 챗에서의 챗
async def chat_completion_classroom_deprecated(user_id: str, msg, classroom_id: str):
    user = await collection.find_one({"id": user_id})
    if not user:
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
    res_msg = chat_response.choices[0].message.content

    try:
        parsed_msg = json.loads(res_msg)
        # If parsing is successful, treat msg as JSON
        for concept_data in parsed_msg:
            concept_id = str(uuid.uuid4())
            concept = {"name": concept_data["name"], "conceptId": concept_id, "chatList": []}
            classroom["conceptList"].append(concept)

    except json.JSONDecodeError:
        normal_res = {"id": str(uuid.uuid4()),"role": "assistant", "content": res_msg}
        target_classroom["chatList"].append(normal_res)


    await collection.update_one(
        {"id": user_id},
        {"$set": {"classroomList": user["classroomList"]}}
    )
    return target_classroom["chatList"]

#이름 바꾸기
async def get_sample_chat(id:str, classroom_id:str):

    pipeline = [
        {"$unwind": "$classroomList"},  # Unwind the classroomList array
        {"$match": {"classroomList.classroomId": classroom_id}},  # Match documents with the given ID
        {"$replaceRoot": {"newRoot": "$classroomList"}},  # Replace root with the inner_structure
        {"$project": {"classroomName":0, "classroomId":0,"conceptList":0, "chatList": { "id": 0}}}
    ]
    
    result = await collection.aggregate(pipeline).to_list(None)
    
    if not result:
        raise HTTPException(status_code=404, detail="Inner structure not found")

    chats_to_send = result[0]["chatList"]

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
    
    concept_list = [{"id": concept["conceptId"], "name": concept["name"]} for concept in target_classroom["conceptList"]]
    
    return concept_list

async def get_concept_list():
    course_name = 'Computer Algorithm'
    client = openai_config()
    json_response = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[
    {
      "role": "system",
      "content": "You are a Professor of the course above. Please generate a list of essential prerequisites of this course in  specific mathematical concepts, \n narrowed enough to be covered within 20 minutes. \n\nGuidelines to formatting:\n- format : JSON \n- No  code block delimiter. \n- Contain the key \"concepts\" and  then place the concepts in a List format. \n- example : \n{\"concepts\": [ \n{\"name\": \"concept1\"}, \n{\"name\": \"concept2\"},\n{\"name\": \"concept3\"},\n ]}"
    },
    {
      "role": "user",
      "content": "I want to take a 'Computer Algorithm' course. "
    },
    {
      "role": "assistant",
      "content": "{\n\"concepts\": [\n{\"name\": \"Basic Programming Constructs\"},\n{\"name\": \"Data Types and Variables\"},\n{\"name\": \"Control Structures (if-else, loops)\"},\n{\"name\": \"Functions and Recursion\"},\n{\"name\": \"Basic Data Structures (Arrays, Lists)\"},\n{\"name\": \"Complexity and Big O Notation\"},\n{\"name\": \"Basic Sorting Algorithms (e.g., Bubble Sort, Selection Sort)\"},\n{\"name\": \"Basic Searching Algorithms (e.g., Linear Search, Binary Search)\"}\n]}"
    }
  ],
  temperature=0.2,
  max_tokens=960,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
    print('!!!!!!!!!!!!!!!!!!')
    print(json_response.choices[0].message.content)
    return json_response.choices[0].message.content




