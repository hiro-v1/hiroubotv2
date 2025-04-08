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
        print(f"[LOG] Pengguna {user_id} ditambahkan ke daftar premium.")
    return True

async def remove_prem(user_id):
    prem_list = await get_prem()
    if user_id in prem_list:
        prem_list.remove(user_id)
        await user.update_one({"prem": "prem"}, {"$set": {"list": prem_list}}, upsert=True)
    return True

async def set_expired_date(user_id, expired_date):
    await user.update_one(
        {"user_id": user_id},
        {"$set": {"expired_date": expired_date}},
        upsert=True,
    )

async def is_reseller(user_id):
    """Cek apakah pengguna adalah reseller."""
    prem_data = await user.find_one({"prem": "prem"})
    return user_id in prem_data.get("resellers", []) if prem_data else False

async def add_reseller(user_id):
    """Tambahkan pengguna sebagai reseller."""
    prem_data = await user.find_one({"prem": "prem"})
    resellers = prem_data.get("resellers", []) if prem_data else []
    if user_id not in resellers:
        resellers.append(user_id)
        await user.update_one({"prem": "prem"}, {"$set": {"resellers": resellers}}, upsert=True)

async def remove_reseller(user_id):
    """Hapus pengguna dari daftar reseller."""
    prem_data = await user.find_one({"prem": "prem"})
    resellers = prem_data.get("resellers", []) if prem_data else []
    if user_id in resellers:
        resellers.remove(user_id)
        await user.update_one({"prem": "prem"}, {"$set": {"resellers": resellers}}, upsert=True)

async def is_trial_used(user_id):
    result = await trialdb.find_one({"user_id": user_id})
    print(f"[LOG] Cek trial untuk {user_id}: {'Sudah digunakan' if result else 'Belum digunakan'}")
    return bool(result)
