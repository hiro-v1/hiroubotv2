from DanteUserbot.core.database import mongodb

ubotdb = mongodb.ubot

async def add_ubot(user_id, api_id, api_hash, session_string):
    return await ubotdb.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "api_id": api_id,
                "api_hash": api_hash,
                "session_string": session_string,
            }
        },
        upsert=True,
    )

async def remove_ubot(user_id):
    return await ubotdb.delete_one({"user_id": user_id})

async def get_DanteUserbots():
    data = []
    async for ubot in ubotdb.find({"user_id": {"$exists": 1}}):
        data.append(
            dict(
                name=str(ubot["user_id"]),  # Ubah kunci 'user_id' menjadi 'name'
                api_id=ubot["api_id"],
                api_hash=ubot["api_hash"],
                session_string=ubot["session_string"],
            )
        )
    return data

async def get_expired_date(user_id):
    """
    Retrieve the expiration date for a user.
    """
    user_data = await ubotdb.find_one({"user_id": user_id}, {"_id": 0, "expired_date": 1})
    return user_data.get("expired_date") if user_data else None
