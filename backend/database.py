from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.mongo_db_name]

users_collection = db["users"]
expenses_collection = db["expenses"]
categories_collection = db["categories"]

DEFAULT_CATEGORIES = [
    "Food", "Transport", "Rent", "Utilities", "Shopping",
    "Entertainment", "Health", "Education", "Travel", "Other",
]


async def ensure_indexes():
    """Call this once on startup to set up indexes and default data."""
    await users_collection.create_index("email", unique=True)
    await expenses_collection.create_index("user_id")
    await expenses_collection.create_index("date")
