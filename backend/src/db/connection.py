# MongoDB driver
import motor.motor_asyncio
from ..models.user import User


#이 파일과 mongoDB 연결
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
database = client.Test

# SQL table이랑 같은 개념
collection = database.users

async def create_user(user):
    document = user
    result = await collection.insert_one(document)
    return document