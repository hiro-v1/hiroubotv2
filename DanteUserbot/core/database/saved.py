from DanteUserbot.core.database import mongodb

varsdb = mongodb.vars

async def set_vars(user_id, vars_name, value, query="vars"):
    try:
        update_data = {"$set": {f"{query}.{vars_name}": value}}
        await varsdb.update_one({"_id": user_id}, update_data, upsert=True)
    except Exception as e:
        print(f"Error setting vars: {e}")

async def get_vars(user_id, vars_name, query="vars"):
    try:
        result = await varsdb.find_one({"_id": user_id})
        return result.get(query, {}).get(vars_name, None) if result else None
    except Exception as e:
        print(f"Error getting vars: {e}")
        return None

async def remove_vars(user_id, vars_name, query="vars"):
    try:
        remove_data = {"$unset": {f"{query}.{vars_name}": ""}}
        await varsdb.update_one({"_id": user_id}, remove_data)
    except Exception as e:
        print(f"Error removing vars: {e}")

async def all_vars(user_id, query="vars"):
    try:
        result = await varsdb.find_one({"_id": user_id})
        return result.get(query) if result else None
    except Exception as e:
        print(f"Error getting all vars: {e}")
        return None

async def remove_all_vars(user_id):
    try:
        await varsdb.delete_one({"_id": user_id})
    except Exception as e:
        print(f"Error removing all vars: {e}")

async def set_status(user_id, status):
    await set_vars(user_id, "WORD_DETECTION_STATUS", status)

async def get_status(user_id):
    status = await get_vars(user_id, "WORD_DETECTION_STATUS")
    return status if status is not None else False

async def get_list_from_vars(user_id, vars_name, query="vars"):
    vars_data = await get_vars(user_id, vars_name, query)
    return [int(x) for x in str(vars_data).split()] if vars_data else []

async def add_to_vars(user_id, vars_name, value, query="vars"):
    vars_list = await get_list_from_vars(user_id, vars_name, query)
    if value not in vars_list:
        vars_list.append(value)
        await set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)

async def remove_from_vars(user_id, vars_name, value, query="vars"):
    vars_list = await get_list_from_vars(user_id, vars_name, query)
    if value in vars_list:
        vars_list.remove(value)
        await set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)

async def get_pm_id(user_id):
    pm_id = await get_vars(user_id, "PM_PERMIT")
    return [int(x) for x in str(pm_id).split()] if pm_id else []

async def add_pm_id(me_id, user_id):
    pm_id = await get_vars(me_id, "PM_PERMIT")
    if pm_id:
        user_id = f"{pm_id} {user_id}"
    await set_vars(me_id, "PM_PERMIT", user_id)

async def remove_pm_id(me_id, user_id):
    pm_id = await get_vars(me_id, "PM_PERMIT")
    if pm_id:
        list_id = [int(x) for x in str(pm_id).split() if x != str(user_id)]
        await set_vars(me_id, "PM_PERMIT", " ".join(map(str, list_id)))
