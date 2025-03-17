from HiroUserbot.core.database import mongodb

bcastdb = mongodb.bcastdb


async def is_served_user(user_id: int) -> bool:
    user = await bcastdb.find_one({"user_id": user_id, "has_started": True})
    if not user:
        return False
    return True

async def get_served_users() -> list:
    users_list = []
    async for user in bcastdb.find({"user_id": {"$gt": 0}, "has_started": True}):
        users_list.append(user)
    return users_list

async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await bcastdb.insert_one({"user_id": user_id, "has_started": True})