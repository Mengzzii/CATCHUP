import uuid
from fastapi import HTTPException
from ..db.connection import collection
from .langchain_controllers import (langchain_learningmaterial, langchain_qna)

# 학습 자료 제공용 chat_completion
# 개념 챗방에서 학습 자료를 생성하고 제공해줌
# contextlist[1], vectorDB 접근 O
async def chat_completion_supplement(user_id: str, classroom_id, concept_id):
    pipeline = [
        {"$unwind": "$classroomList"},  # Unwind the classroomList array
        {"$match": {"classroomList.classroomId": classroom_id}},  # Match documents with the given ID
        {"$unwind": "$classroomList.conceptList"},  # Unwind the conceptList array
        {"$match": {"classroomList.conceptList.conceptId": concept_id}},
        {"$replaceRoot": {"newRoot": "$classroomList.conceptList"}},  # Replace root with the inner_structure
        {"$project": { "conceptId": 0, "chatList": {"id": 0 }}} # 안쓰는 필드 출력에서 제외
    ]
    
    result = await collection.aggregate(pipeline).to_list(None)
    
    if not result:
        raise HTTPException(status_code=404, detail="Inner structure not found")

    chats_to_send = result[0]["chatList"]
    concept = result[0]["name"]
    print(concept)
    res = await langchain_learningmaterial(1, concept)

    #제공한 학습자료를 DB에 저장
    ## 1. format
    db_res = {"id": str(uuid.uuid4()),"content": res, "role": "assistant"}
    ## 2. update
    updated_user = await collection.update_one(
        {"classroomList.classroomId": classroom_id},
        {"$push": {"classroomList.$.conceptList.$[concept].chatList": {"$each":[db_res]}}},
        array_filters=[{"concept.conceptId": concept_id}]
    )

    if updated_user.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    # Return Updated Chatlist
    chats_to_send.append({"content": res, "role": "assistant"})
    return chats_to_send

# Q&A chat_completion
# 개념 챗방에서 사용자의 질문에 대한 답변 해줌
# contextlist[2], vectorDB 접근 X
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

    chats_to_send = result[0]["chatList"]

    question = msg
    previous_chat = " "+", ".join([chat['content'] for chat in chats_to_send])
    res = await langchain_qna(2, question, previous_chat)

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
    chats_to_send.append({"content": msg, "role": "user"})
    chats_to_send.append({"content": res, "role": "assistant"})
    return chats_to_send