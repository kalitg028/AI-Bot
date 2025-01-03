import motor.motor_asyncio
from info import DATABASE_URL, DATABASE_NAME

class Database:
    def __init__(self, url, database_name):
        # Initialize the MongoDB client
        self._client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.db = self._client[database_name]
        self.col = self.db.users  # Collection where users are stored

    # Method to create a new user dictionary
    def new_user(self, user_id):
        return {"id": user_id}

    # Method to add a new user
    async def add_user(self, user_id):
        user = self.new_user(user_id)
        # Insert user into the database
        await self.col.insert_one(user)

    # Check if a user exists by user_id
    async def is_user_exist(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        return True if user else False

    # Get the total count of users
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    # Get all users from the database (returns a list)
    async def get_all_users(self):
        all_users_cursor = self.col.find({})
        all_users = []
        async for user in all_users_cursor:
            all_users.append(user)
        return all_users

    # Delete a user by user_id
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

# Initialize the database object
db = Database(DATABASE_URL, DATABASE_NAME)
