from typing import Any
from config import DB_URI, DB_NAME
from motor import motor_asyncio
from datetime import datetime, timedelta
client: motor_asyncio.AsyncIOMotorClient[Any] = motor_asyncio.AsyncIOMotorClient(DB_URI)
db = client[DB_NAME]

class Techifybots:
    def __init__(self):
        self.users = db["users"]
        self.cache : dict[int, dict[str, Any]] = {}

    async def add_user(self, user_id: int, name: str) -> dict[str, Any] | None:
        try:
            user: dict[str, Any] = {"user_id": user_id, "name": name}
            await self.users.insert_one(user)
            self.cache[user_id] = user      
            return user
        except Exception as e:
            print("Error in addUser: ", e)
            

    async def get_user(self, user_id: int) -> dict[str, Any] | None:
        try:
            if user_id in self.cache:
                return self.cache[user_id]
            user = await self.users.find_one({"user_id": user_id})
            return user
        except Exception as e:
            print("Error in getUser: ", e)
            return None
    
    async def get_all_users(self) -> list[dict[str, Any]]:
        try:
            users : list[dict[str, Any]] = []
            async for user in self.users.find():
                users.append(user)
            return users
        except Exception as e:
            print("Error in getAllUsers: ", e)
            return []

    async def get_active_users_today(self) -> int:
        try:
            today = datetime.utcnow() - timedelta(days=1)
            return await self.users.count_documents({"last_active": {"$gte": today}})
        except Exception as e:
            print("Error in get_active_users_today: ", e)
            return 0

    async def update_user_activity(self, user_id: int) -> None:
        try:
            await self.users.update_one(
                {"user_id": user_id},
                {"$set": {"last_active": datetime.utcnow()}}
            )
        except Exception as e:
            print("Error in update_user_activity: ", e)

tb = Techifybots()
