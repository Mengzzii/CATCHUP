import uuid
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