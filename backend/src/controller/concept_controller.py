import uuid
import json
from fastapi import HTTPException
from ..db.connection import collection

async def store_concept(user_id, classroom_id):
    user = await collection.find_one({"id":user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    classroom = None
    for clsrm in user["classroomList"]:
        if clsrm["classroomId"] == classroom_id:
            classroom = clsrm
            break
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    concepts_data = [
        {"name": "Algorithm Analysis"},
        {"name": "Time Complexity"},
        {"name": "Space Complexity"},
        {"name": "Pseudocode"},
        {"name": "Big-O Notation"},
        {"name": "Sorting Algorithms"},
        {"name": "Bubble Sort"},
        {"name": "Selection Sort"},
        {"name": "Merge Sort"},
        {"name": "Quick Sort"},
        {"name": "Radix Sort"},]

    for concept_data in concepts_data:
        concept_id = str(uuid.uuid4())
        concept = {"name": concept_data["name"], "conceptId": concept_id, "chatList": []}
        classroom["conceptList"].append(concept)

    await collection.update_one(
    {"id": user_id},
    {"$set": {"classroomList": user["classroomList"]}}
    )

    return [concept["conceptId"] for concept in classroom["conceptList"]]


async def chat_check_store(user_id, classroom_id, msg):
    user = await collection.find_one({"id":user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    classroom = None
    for clsrm in user["classroomList"]:
        if clsrm["classroomId"] == classroom_id:
            classroom = clsrm
            break
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    try:
        parsed_msg = json.loads(msg)
        # If parsing is successful, treat msg as JSON
        for concept_data in parsed_msg:
            concept_id = str(uuid.uuid4())
            concept = {"name": concept_data["name"], "conceptId": concept_id, "chatList": []}
            classroom["conceptList"].append(concept)

    except json.JSONDecodeError:
        # If JSON decoding fails, treat msg as a regular message
        chat_id = str(uuid.uuid4())
        chat_role = "assistant"
        msg_as_chat = {"id": chat_id, "role": chat_role, "content": msg}
        classroom["chatList"].append(msg_as_chat)

    await collection.update_one(
        {"id": user_id},
        {"$set": {"classroomList": user["classroomList"]}}
    )

    return {"message": "It is JSON" if 'parsed_msg' in locals() else "It is message"} 
