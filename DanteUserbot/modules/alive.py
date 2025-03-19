from DanteUserbot import *
import psutil
import asyncio
from datetime import datetime
from pyrogram.enums import *
from os import getpid
from time import time
from DanteUserbot.core.database.permit import *
from DanteUserbot.core.helpers.formatter import *
from pyrogram.raw.functions import Ping
from pyrogram.types import (InlineKeyboardMarkup, InlineQueryResultArticle,
                            InputTextMessageContent, InlineKeyboardButton)
from DanteUserbot.core.helpers.unpack import unpackInlineMessage
from DanteUserbot.core.helpers.client import DANTE  # Import DANTE to access INLINE
from DanteUserbot.core.decorators import INLINE  # Ensure INLINE is imported from the correct module

# Caching untuk menghindari pengambilan data berulang
dialog_cache = {}

async def get_dialog_counts(bot_id, client):
    """Menghitung jumlah users dan groups dengan caching (5 menit)."""
    now = time()
    if bot_id in dialog_cache and now - dialog_cache[bot_id]["timestamp"] < 300:
        return dialog_cache[bot_id]["users"], dialog_cache[bot_id]["groups"]

    users, groups = 0, 0
    async for dialog in client.get_dialogs(limit=None):
        if dialog.chat.type == ChatType.PRIVATE:
            users += 1
        elif dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            groups += 1

    dialog_cache[bot_id] = {"users": users, "groups": groups, "timestamp": now}
    return users, groups

@DANTE.CALLBACK("sys_stats")
@INLINE.DATA
async def _sys_callback(client, cq):
    """Menampilkan statistik sistem saat tombol 'stats' ditekan."""
    text = sys_stats()
    await bot.answer_callback_query(cq.id, text, show_alert=True)

def sys_stats():
    """Mengambil statistik sistem bot (CPU, RAM, Disk, Uptime)."""
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(getpid())
    return f"""
-----------------------
ᴜᴘᴛɪᴍᴇ: {time_formatter((time() - start_time) * 1000)}
ʙᴏᴛ ʀᴀᴍ ᴜsᴀɢᴇ: {round(process.memory_info()[0] / 1024 ** 2)} MB
ᴄᴘᴜ ᴜsᴀɢᴇ: {cpu}%
ʀᴀᴍ ᴜsᴀɢᴇ: {mem}%
ᴅɪsᴋ ᴜsᴀɢᴇ: {disk}%
-----------------------
"""

@DANTE.UBOT("alive")
async def alive_cmd(client, message):
    """Command untuk menampilkan status bot secara inline."""
    x = await client.get_inline_bot_results(
        bot.me.username, f"alive {message.id} {client.me.id}"
    )
    await message.reply_inline_bot_result(x.query_id, x.results[0].id, quote=True)

@DANTE.INLINE("^alive")
async def alive_inline_handler(client, inline_query):
    """Menampilkan status bot dalam mode inline dengan `get_dialog_counts()`."""
    try:
        get_id = inline_query.query.split()
        user_id = int(get_id[2])

        for my in ubot._ubot:
            if user_id == my.me.id:
                # Menggunakan get_dialog_counts untuk menghitung jumlah users dan groups
                users, groups = await get_dialog_counts(my.me.id, my)

                get_exp = await get_expired_date(my.me.id)
                expired = f"<code>{get_exp.strftime('%d-%m-%Y')}</code>" if get_exp else ""
                status = "**official**" if my.me.id == OWNER_ID else "**unofficial**"
                antipm = "enable" if await get_vars(my.me.id, "ENABLE_PM_GUARD") else "disable"

                button = [[
                    InlineKeyboardButton("Tutup", callback_data=f"alv_cls {int(get_id[1])} {user_id}"),
                    InlineKeyboardButton("Stats", callback_data="sys_stats"),
                ]]

                start = datetime.now()
                await my.invoke(Ping(ping_id=0))
                ping = (datetime.now() - start).microseconds / 1000
                uptime = await get_time(time() - start_time)

                msg = f"""
<b>hirov1-ᴜsᴇʀʙᴏᴛ Os</b>
     <b>Status:</b> [{status}]
     <b>Device Model:</b> <code>Sᴡᴇᴇᴛ</code>
     <b>Magisk Hide:</b> <code>{antipm}</code>
     <b>Magisk Module:</b> <code>{len(ubot._ubot)}</code>
     <b>CPU Model:</b> <code>hiroRTX-Gforce</code>
     <b>Kernel Version:</b> <code>ɢᴇɴᴏᴍ R{groups}-{users}</code>
     <b>Device Version:</b> <code>14.0.2</code>
     <b>Baseband Version:</b> <code>Unknown</code>
     <b>Device Ping:</b> <code>{ping}</code>
     <b>Device Uptime:</b> <code>{uptime}</code>
     <b>Security Patch:</b> {expired}
"""

                await client.answer_inline_query(
                    inline_query.id,
                    cache_time=300,
                    results=[
                        InlineQueryResultArticle(
                            title="💬",
                            reply_markup=InlineKeyboardMarkup(button),
                            input_message_content=InputTextMessageContent(msg),
                        )
                    ],
                )
                return

    except (IndexError, ValueError):
        await client.answer_inline_query(
            inline_query.id,
            cache_time=5,
            results=[
                InlineQueryResultArticle(
                    title="⚠️ Error",
                    input_message_content=InputTextMessageContent("Format query salah atau user tidak ditemukan."),
                )
            ],
        )

@DANTE.CALLBACK("alv_cls")
@INLINE.DATA
async def alive_close(client, callback_query):
    """Menutup pesan alive inline."""
    get_id = callback_query.data.split()
    if callback_query.from_user.id != int(get_id[2]):
        return await callback_query.answer(
            f"❌ Tombol ini bukan untukmu, {callback_query.from_user.first_name}.",
            True,
        )

    unPacked = unpackInlineMessage(callback_query.inline_message_id)
    for my in ubot._ubot:
        if callback_query.from_user.id == int(my.me.id):
            await my.delete_messages(unPacked.chat_id, [int(get_id[1]), unPacked.message_id])
