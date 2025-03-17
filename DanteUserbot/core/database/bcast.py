from datetime import datetime
from DanteUserbot.core.database import mongodb

bcastdb = mongodb.bcastdb
blacklistdb = mongodb.blacklistdb
autogikesdb = mongodb.autogikesdb


async def is_served_user(user_id: int) -> bool:
    """Cek apakah user sudah terdaftar dalam database."""
    return await bcastdb.find_one({"user_id": user_id, "has_started": True}, {"_id": 0}) is not None

async def get_served_users() -> list:
    """Mengembalikan daftar user yang sudah terdaftar dengan metadata."""
    return [
        {"user_id": user["user_id"], "added_at": user.get("added_at")}
        async for user in bcastdb.find({"user_id": {"$gt": 0}, "has_started": True}, {"_id": 0, "user_id": 1, "added_at": 1})
    ]

async def get_served_users_list() -> list:
    """Mengembalikan hanya daftar user_id tanpa metadata."""
    return [
        user["user_id"]
        async for user in bcastdb.find({"user_id": {"$gt": 0}, "has_started": True}, {"_id": 0, "user_id": 1})
    ]

async def add_served_user(user_id: int):
    """Menambahkan user ke dalam database jika belum ada."""
    if not await is_served_user(user_id):
        await bcastdb.insert_one({
            "user_id": user_id,
            "has_started": True,
            "added_at": datetime.utcnow()
        })


async def is_blacklisted(chat_id: int) -> bool:
    """Cek apakah chat termasuk dalam blacklist."""
    return await blacklistdb.find_one({"chat_id": chat_id}, {"_id": 0}) is not None

async def add_blacklist(chat_id: int):
    """Menambahkan chat ke dalam blacklist jika belum ada."""
    if not await is_blacklisted(chat_id):
        await blacklistdb.insert_one({
            "chat_id": chat_id,
            "blacklisted_at": datetime.utcnow()
        })

async def remove_blacklist(chat_id: int):
    """Menghapus satu chat dari blacklist."""
    await blacklistdb.delete_one({"chat_id": chat_id})

async def clear_blacklist():
    """Menghapus semua data blacklist dari database."""
    await blacklistdb.delete_many({})

async def get_blacklist() -> list:
    """Mengembalikan daftar semua chat yang masuk blacklist dengan metadata."""
    return [
        {"chat_id": chat["chat_id"], "blacklisted_at": chat.get("blacklisted_at")}
        async for chat in blacklistdb.find({}, {"_id": 0, "chat_id": 1, "blacklisted_at": 1})
    ]


async def set_autogikes(user_id: int, text: str, target: str, delay: int, limit: int):
    """Menyimpan atau memperbarui pengaturan AutoGikes."""
    await autogikesdb.update_one(
        {"user_id": user_id},
        {"$set": {
            "text": text,
            "target": target,
            "delay": delay,
            "limit": limit,
            "last_updated": datetime.utcnow()
        }},
        upsert=True
    )

async def get_autogikes(user_id: int):
    """Mengambil data AutoGikes berdasarkan user_id."""
    data = await autogikesdb.find_one({"user_id": user_id}, {"_id": 0})
    return data if data else None

async def remove_autogikes(user_id: int):
    """Menghapus AutoGikes berdasarkan user_id."""
    await autogikesdb.delete_one({"user_id": user_id})

async def remove_all_autogikes():
    """Menghapus semua pengaturan AutoGikes dalam database."""
    await autogikesdb.delete_many({})
