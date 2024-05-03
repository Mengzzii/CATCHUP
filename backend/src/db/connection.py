# MongoDB 연결
import motor.motor_asyncio

from dotenv import load_dotenv
import os
load_dotenv()

user = os.environ.get("MONGODB_USER_NAME")
password = os.environ.get("MONGODB_PASSWORD")

MONGO_URL = f"mongodb+srv://{user}:{password}@cluster0.dy560h4.mongodb.net/"

# 이 파일과 MongoDB 연결
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.Test

# SQL table이랑 같은 개념
collection = database.users