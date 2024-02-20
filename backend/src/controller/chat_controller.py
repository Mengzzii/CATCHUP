from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# async def update_todo(title, desc):
#     await collection.update_one({"title": title}, {"$set": {"description": desc}})
#     document = await collection.find_one({"title": title})
#     return document

def openai_config():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    return client


#print(completion.choices[0].message)

## get user id
## grab chats of user



