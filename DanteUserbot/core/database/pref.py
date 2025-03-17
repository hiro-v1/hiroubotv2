from DanteUserbot.core.database import mongodb

prefixes = mongodb["DanteUserbot"]["prefix"]

async def get_pref(user_id):
    sh = await prefixes.find_one({"_id": user_id})
    if sh:
        return sh.get("prefixesi")
    else:
        return "."

async def set_pref(user_id, prefix):
    await prefixes.update_one(
        {"_id": user_id}, {"$set": {"prefixesi": prefix}}, upsert=True
    )

async def rem_pref(user_id):
    await prefixes.update_one(
        {"_id": user_id}, {"$unset": {"prefixesi": ""}}, upsert=True
    )
