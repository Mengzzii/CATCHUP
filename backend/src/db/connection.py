# MongoDB driver
import motor.motor_asyncio
from ..models.user import User

from dotenv import load_dotenv
import os
load_dotenv()

user = os.environ.get("MONGODB_USER_NAME")
password = os.environ.get("MONGODB_PASSWORD")

MONGO_URL = f"mongodb+srv://{user}:{password}@cluster0.dy560h4.mongodb.net/"

#이 파일과 mongoDB 연결
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.Test

# SQL table이랑 같은 개념
collection = database.users

# async def create_user(user):
#     document = user
#     result = await collection.insert_one(document)
#     return document