import asyncio
from typing import Dict, List, Union
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import filters
from ...config import MONGO_URL

# Menghubungkan ke MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.hiro_userbot
gmute = mongodb.gmute  # Pastikan ini sesuai dengan koleksi yang Anda maksud
filtersdb = mongodb.filters  # Pastikan ini sesuai dengan koleksi yang Anda maksud

async def get_gmuteh_users(gua: int) -> List[int]:
    results = []
    async for user in gmute.find({"gua": gua, "user_id": {"$gt": 0}}):
        results.append(user["user_id"])
    return results

async def get_gmuteh_count(gua: int) -> int:
    return await gmute.count_documents({"gua": gua, "user_id": {"$gt": 0}})

async def is_gmuteh_user(gua: int, user_id: int) -> bool:
    user = await gmute.find_one({"gua": gua, "user_id": user_id})
    return bool(user)

async def add_gmuteh_user(gua: int, user_id: int):
    if not await is_gmuteh_user(gua, user_id):
        await gmute.insert_one({"gua": gua, "user_id": user_id})

async def remove_gmuteh_user(gua: int, user_id: int):
    if await is_gmuteh_user(gua, user_id):
        await gmute.delete_one({"gua": gua, "user_id": user_id})

async def get_filters_count() -> Dict[str, int]:
    chats_count = 0
    filters_count = 0
    async for chat in filtersdb.find({"chat_id": {"$lt": 0}}):
        filters_name = await get_filters_names(chat["user_id"], chat["chat_id"])
        filters_count += len(filters_name)
        chats_count += 1
    return {
        "chats_count": chats_count,
        "filters_count": filters_count,
    }

async def _get_filters(user_id: int, chat_id: int) -> Dict[str, int]:
    _filters = await filtersdb.find_one({"user_id": user_id, "chat_id": chat_id})
    return _filters["filters"] if _filters else {}

async def get_filters_names(user_id: int, chat_id: int) -> List[str]:
    _filters = await _get_filters(user_id, chat_id)
    return list(_filters.keys())

async def get_filter(user_id: int, chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    _filters = await _get_filters(user_id, chat_id)
    return _filters.get(name, False)

async def save_filter(user_id: int, chat_id: int, name: str, _filter: dict):
    name = name.lower().strip()
    _filters = await _get_filters(user_id, chat_id)
    _filters[name] = _filter
    await filtersdb.update_one(
        {"user_id": user_id, "chat_id": chat_id},
        {"$set": {"filters": _filters}},
        upsert=True,
    )

async def delete_filter(user_id: int, chat_id: int, name: str) -> bool:
    filtersd = await _get_filters(user_id, chat_id)
    name = name.lower().strip()
    if name in filtersd:
        del filtersd[name]
        await filtersdb.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$set": {"filters": filtersd}},
            upsert=True,
        )
        return True
    return False