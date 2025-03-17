from DanteUserbot.core.database import mongodb

user = mongodb.premium

async def get_prem():
    prem = await user.find_one({"prem": "prem"})
    if not prem:
        return []
    return prem["list"]

async def add_prem(user_id):
    prem_list = await get_prem()
    if user_id not in prem_list:
        prem_list.append(user_id)
        await user.update_one({"prem": "prem"}, {"$set": {"list": prem_list}}, upsert=True)
    return True

async def remove_prem(user_id):
    prem_list = await get_prem()
    if user_id in prem_list:
        prem_list.remove(user_id)
        await user.update_one({"prem": "prem"}, {"$set": {"list": prem_list}}, upsert=True)
    return True
