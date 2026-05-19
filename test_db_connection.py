from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

from services.config import MONGO_URI

async def test_connection():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_database("pic_up")
    print(await db.list_collection_names())  # מציג רשימת קולקציות
    await client.close()

asyncio.run(test_connection())