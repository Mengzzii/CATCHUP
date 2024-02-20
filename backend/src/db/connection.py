# MongoDB driver
import motor.motor_asyncio
from ..models.user import User
from ..controller.chat_controller import (openai_config)

password = 'GuNUsjOAYfcdvChC'
MONGO_URL = f"mongodb+srv://test:{password}@cluster0.dy560h4.mongodb.net/"

#이 파일과 mongoDB 연결
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.Test

# SQL table이랑 같은 개념
collection = database.users

async def create_user(user):
    document = user
    result = await collection.insert_one(document)
    return document

async def chat_completion(user, msg):
    # grab chats of user
    chats = [{"role": chat.role, "content": chat.content} for chat in user.chats]
    chats.append({"content": msg, "role": "user"})
    user.chats.append({"content": msg, "role": "user"})
    print(user.chats)

    # send all chats with new one to openAI API
    client = openai_config()

    # get latest response
    chat_response = await client.chat.completions.create( model="gpt-3.5-turbo", messages=chats)
    user.chats.append(chat_response.data.choices[0].message)
    await user.save()
    return user