from datetime import datetime
from pytz import timezone
from DanteUserbot.core.database import mongodb
from DanteUserbot.core.database.DanteUserbot import get_expired_date  # Impor untuk cek expired

trialdb = mongodb.trialdb  # Koleksi untuk menyimpan pengguna yang sudah coba gratis
trial_db = mongodb.trial_users

async def is_trial_used(user_id: int) -> bool:
    return bool(await trialdb.find_one({"user_id": user_id}))
    
async def mark_trial_used(user_id: int):
    await trialdb.insert_one({"user_id": user_id, "used_at": datetime.now(timezone("Asia/Jakarta"))})

async def clear_expired_trials():
    now = datetime.now(timezone("Asia/Jakarta"))
    async for user in trialdb.find():
        user_id = user["user_id"]
        expired_date = await get_expired_date(user_id)
        if not expired_date or expired_date < now:  # Jika masa aktif habis
            await trialdb.delete_one({"user_id": user_id})

async def is_trial_used(user_id):
    return await trial_db.find_one({"user_id": user_id}) is not None

async def mark_trial_used(user_id):
    await trial_db.update_one({"user_id": user_id}, {"$set": {"used": True}}, upsert=True)
