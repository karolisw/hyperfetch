# This is the reusable connection that will be used throughout the application
# The client is properly instantiated when main.py runs
from motor.motor_asyncio import AsyncIOMotorClient


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client
