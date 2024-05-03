from ..db.connection import collection
from fastapi import HTTPException
import uuid
from .langchain_controllers import (langchain_conceptlist)
import json

# 개념 리스트 반환 chat_completion
# 기본 챗방에서 사용자가 어떤 과목을 듣고 싶다 입력시 관련 선수학습사항 개념리스트 반환
# contextlist[0], vectorDB 접근 고민중
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

# 기본 챗방 챗팅 반환 함수
# 해당 classroom_id의 채팅 기록을 반환해줌
async def get_classroom_chat(id:str, classroom_id:str):

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

# 개념 챗방 챗팅 반환 함수
# 해당 classroom_id 내에있는 해당 concept_id의 채팅 기록을 반환해줌
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

# 개념리스트 반환 함수
# 해당 classroom_id에 있는 concept_list를 반환해줌
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