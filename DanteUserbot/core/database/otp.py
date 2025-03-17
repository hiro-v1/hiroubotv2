from DanteUserbot.core.database import mongodb

getopt = mongodb["DanteUserbot"]["twofactor"]

async def get_two_factor(user_id):
    user = await getopt.find_one({"_id": user_id})
    if user:
        return user.get("twofactor")
    else:
        return None

async def set_two_factor(user_id, twofactor):
    await getopt.update_one(
        {"_id": user_id}, {"$set": {"twofactor": twofactor}}, upsert=True
    )

async def rem_two_factor(user_id):
    await getopt.update_one(
        {"_id": user_id}, {"$unset": {"twofactor": ""}}, upsert=True
    )
