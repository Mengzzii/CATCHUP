import uuid
import json
from fastapi import HTTPException
from ..config.openai_config import openai_config
from ..db.connection import collection
#from .concept_controller import (langchain_learningmaterial, langchain_qna)

#학습 자료 제공용 chat_completion
#contextlist 1
#vectorDB 접근 O
#user_id를 안쓰고 어떻게 classroomList를 펼치는걸까? classroom_id가 고유해서 괜찮은건가??
async def chat_completion_supplement(user_id: str, msg, classroom_id, concept_id):
    pipeline = [
        {"$unwind": "$classroomList"},  # Unwind the classroomList array
        {"$match": {"classroomList.classroomId": classroom_id}},  # Match documents with the given ID
        {"$unwind": "$classroomList.conceptList"},  # Unwind the conceptList array
        {"$match": {"classroomList.conceptList.conceptId": concept_id}},
        {"$replaceRoot": {"newRoot": "$classroomList.conceptList"}},  # Replace root with the inner_structure
        {"$project": { "name": 0, "conceptId": 0, "chatList": {"id": 0 }}} # 안쓰는 필드 출력에서 제외
    ]
    
    result = await collection.aggregate(pipeline).to_list(None)
    
    if not result:
        raise HTTPException(status_code=404, detail="Inner structure not found")

    # Send all chats with new one to openAI API
    chats_to_send = result[0]["chatList"]
    chats_to_send.append({"content": msg, "role": "user"})

    ###############
    client = openai_config()
    res = client.chat.completions.create( model="gpt-3.5-turbo", messages=chats_to_send).choices[0].message.content
    chats_to_send.append({"content": res, "role": "assistant"})
    ###############
    #langchain_learningmaterial(1, concept)

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

#기본 Q&A용 chat_completion
#contextlist 2
#vectorDB 접근 X
async def chat_completion_qna(user_id: str, msg, classroom_id, concept_id):
    pipeline = [
        {"$unwind": "$classroomList"},  # Unwind the classroomList array
        {"$match": {"classroomList.classroomId": classroom_id}},  # Match documents with the given ID
        {"$unwind": "$classroomList.conceptList"},  # Unwind the conceptList array
        {"$match": {"classroomList.conceptList.conceptId": concept_id}},
        {"$replaceRoot": {"newRoot": "$classroomList.conceptList"}},  # Replace root with the inner_structure
        {"$project": { "name": 0, "conceptId": 0, "chatList": {"id": 0 }}} #안쓰는 필드 출력에서 제외
    ]
    
    result = await collection.aggregate(pipeline).to_list(None)
    
    if not result:
        raise HTTPException(status_code=404, detail="Inner structure not found")

    # Send all chats with new one to openAI API
    chats_to_send = result[0]["chatList"]
    ###############
    chats_to_send.append({"content": msg, "role": "user"})

    client = openai_config()
    res = client.chat.completions.create( model="gpt-3.5-turbo", messages=chats_to_send).choices[0].message.content
    chats_to_send.append({"content": res, "role": "assistant"})
    ###############
    #question = {"content": msg, "role": "user"}
    #res = langchain_qna(2, question, chats_to_send)
    #chats_to_send.append({"content": msg, "role": "user"})
    #chats_to_send.append({"content": res, "role": "assistant"})
    #이때 previous chat의 형식?

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

#기본 챗에서의 챗 - chat controller로 가져가고 import 된 곳 있으면 수정하기
async def chat_completion_classroom(user_id: str, msg, classroom_id: str):
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