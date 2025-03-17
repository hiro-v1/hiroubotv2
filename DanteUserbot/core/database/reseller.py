from DanteUserbot.core.database import mongodb

resell = mongodb.seles

async def get_seles():
    seles = await resell.find_one({"seles": "seles"})
    if not seles:
        return []
    return seles["reseller"]

async def add_seles(user_id):
    reseller = await get_seles()
    if user_id not in reseller:
        reseller.append(user_id)
        await resell.update_one(
            {"seles": "seles"}, {"$set": {"reseller": reseller}}, upsert=True
        )
    return True

async def remove_seles(user_id):
    reseller = await get_seles()
    if user_id in reseller:
        reseller.remove(user_id)
        await resell.update_one(
            {"seles": "seles"}, {"$set": {"reseller": reseller}}, upsert=True
        )
    return True
