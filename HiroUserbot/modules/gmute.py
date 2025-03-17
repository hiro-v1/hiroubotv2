import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.types import ChatPermissions
from HiroUserbot import *
from pyrogram.enums import ChatType
from pyrogram.errors import *

async def get_data_id(client, query):
    chat_types = {
        "global": [ChatType.CHANNEL, ChatType.GROUP, ChatType.SUPERGROUP],
        "all": [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE],
        "group": [ChatType.GROUP, ChatType.SUPERGROUP],
        "users": [ChatType.PRIVATE],
    }
    dialogs = []
    try:
        async for dialog in client.get_dialogs():
            if dialog.chat.type in chat_types.get(query, []):
                dialogs.append(dialog.chat.id)
    except ChannelPrivate:
        pass
    return dialogs

__MODULE__ = "ɢᴍᴜᴛᴇ"
__HELP__ = """
**--Bantuan Untuk Gmute--**

<blockquote><b>
perintah : <code>{0}gmute</code>
    untuk mengemute user dari semua gc yg kmu admin 

perintah : <code>{0}ungmute</code>
    untuk meng ungmute user dari semua gc yg kmu admin</blockquote> 
"""


@HIRO.UBOT("gmute")
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    user_id = await extract_user(message)
    _msg = f"{prs}proceꜱꜱing..."

    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit(f"{ggl}user tidak ditemukan")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    text = "global {}\n\nberhasil: {} chat\ngagal: {} chat\nuser: <a href='tg://user?id={}'>{} {}</a>"
    global_id = await get_data_id(client, "group")
    for dialog in global_id:
        if user.id == OWNER_ID:
            return await Tm.edit(f"{ggl}anda tidak bisa gmute dia karena dia pembuat saya")
        try:
            await client.restrict_chat_member(dialog, user.id, ChatPermissions(can_send_messages=False))
            done += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
            await asyncio.sleep(0.1)
    await message.reply(
        text.format(
            "mute", done, failed, user.id, user.first_name, (user.last_name or "")
        )
    )
    return await Tm.delete()

@HIRO.UBOT("ungmute")
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    user_id = await extract_user(message)
    _msg = f"{prs}proceꜱꜱing..."
    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit(f"{ggl}user tidak ditemukan")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    text = "global {}\n\nberhasil: {} chat\ngagal: {} chat\nuser: <a href='tg://user?id={}'>{} {}</a>"
    global_id = await get_data_id(client, "global")
    for dialog in global_id:
        try:
            await client.restrict_chat_member(dialog, user.id, ChatPermissions(can_send_messages=True))
            done += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
            await asyncio.sleep(0.1)
    await message.reply(
        text.format(
            "ungmuted",
            done,
            failed,
            user.id,
            user.first_name,
            (user.last_name or ""),
        )
    )
    return await Tm.delete()
