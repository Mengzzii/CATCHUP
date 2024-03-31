import uuid
import json
from fastapi import HTTPException
from ..config.openai_config import openai_config
from ..db.connection import collection

#학습 자료 제공용 chat_completion
async def chat_completion_supplement():
    return 0

#기본 Q&A용 chat_completion
async def chat_completion_qna():
    return 0

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