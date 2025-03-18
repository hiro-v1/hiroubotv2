from DanteUserbot.core.database import mongo_client

userEXP = mongo_client["DanteUserbot"]["users"]

async def get_expired_date(user_id):
    user = await userEXP.find_one({"_id": user_id})
    if user:
        return user.get("expire_date")
    else:
        return None

async def set_expired_date(user_id, expire_date):
    await userEXP.update_one(
        {"_id": user_id}, {"$set": {"expire_date": expire_date}}, upsert=True
    )

async def rem_expired_date(user_id):
    await userEXP.update_one(
        {"_id": user_id}, {"$unset": {"expire_date": ""}}, upsert=True
    )

async def remove_chat(chat_id):
    """
    Remove a chat from the database.
    """
    await userEXP.delete_one({"_id": chat_id})

def get_chat(chat_id):
    # Define the function to get chat details from the database
    # Example implementation:
    # return database.get_chat(chat_id)
    pass
