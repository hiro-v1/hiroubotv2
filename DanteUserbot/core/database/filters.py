import requests
import asyncio
from pyrogram import filters
from pyrogram.filters import chat
from typing import Dict, List, Union
from pyrogram.types import Message

from motor.motor_asyncio import AsyncIOMotorClient
from DanteUserbot.config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.dante_userbot
db = mongodb.premium
filtersdb = db.filters
gmute = db.gmute

async def get_gmuteh_users(gua: int) -> list:
    results = []
    async for user in gmute.find({"gua": gua, "user_id": {"$gt": 0}}):
        results.append(user["user_id"])
    return results

async def get_gmuteh_count(gua: int) -> int:
    users = gmute.find({"gua": gua, "user_id": {"$gt": 0}})
    users = await users.to_list(length=100000)
    return len(users)

async def is_gmuteh_user(gua: int, user_id: int) -> bool:
    user = await gmute.find_one({"gua": gua, "user_id": user_id})
    return bool(user)

async def add_gmuteh_user(gua: int, user_id: int):
    is_ggmuteh = await is_gmuteh_user(gua, user_id)
    if is_ggmuteh:
        return
    return await gmute.insert_one({"gua": gua, "user_id": user_id})

async def remove_gmuteh_user(gua: int, user_id: int):
    is_ggmuteh = await is_gmuteh_user(gua, user_id)
    if not is_ggmuteh:
        return
    return await gmute.delete_one({"gua": gua, "user_id": user_id})

async def get_filters_count() -> dict:
    chats_count = 0
    filters_count = 0
    async for chat in filtersdb.find({"chat_id": {"$lt": 0}}):
        filters_name = await get_filters_names(chat["chat_id"])
        filters_count += len(filters_name)
        chats_count += 1
    return {
        "chats_count": chats_count,
        "filters_count": filters_count,
    }

async def _get_filters(user_id: int, chat_id: int) -> Dict[str, int]:
    _filters = await filtersdb.find_one({"user_id": user_id, "chat_id": chat_id})
    if not _filters:
        return {}
    return _filters["filters"]

async def get_filters_names(user_id: int, chat_id: int) -> List[str]:
    _filters = []
    for _filter in await _get_filters(user_id, chat_id):
        _filters.append(_filter)
    return _filters

async def get_filter(user_id: int, chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    _filters = await _get_filters(user_id, chat_id)
    if name in _filters:
        return _filters[name]
    return False

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
