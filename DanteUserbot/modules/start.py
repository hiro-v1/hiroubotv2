from .. import *
import asyncio
from datetime import datetime
from time import time
from gc import get_objects
from DanteUserbot import bot, ubot
from pyrogram.errors.exceptions.bad_request_400 import UserBannedInChannel
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from DanteUserbot.core.helpers.inline import Button
from DanteUserbot.core.helpers.text import MSG
from DanteUserbot.core.database.premium import add_served_user

START_TIME = datetime.utcnow()

TIME_DURATION_UNITS = (
    ("Minggu", 60 * 60 * 24 * 7),
    ("Hari", 60 * 60 * 24),
    ("Jam", 60 * 60),
    ("Menit", 60),
    ("Detik", 1),
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f"{amount} {unit}")
    return ", ".join(parts)

async def pong(client, message):
    start = time()
    pong = await message.edit("Proses...")
    delta_ping = time() - start
    uptime_sec = (datetime.utcnow() - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await pong.edit(
        f"<blockquote><b>❏Userbot\n❏Pong : {delta_ping * 1000:.3f} ms\n❏Bot Uptime : {uptime} </b></blockquote>"
    )

async def send_msg_to_owner(client, message):
    if message.from_user.id == OWNER_ID:
        return
    buttons = [
        [
            InlineKeyboardButton("👤 Profil", callback_data=f"profil {message.from_user.id}"),
            InlineKeyboardButton("💬 Jawab", callback_data=f"jawab_pesan {message.from_user.id}"),
        ],
    ]
    await client.send_message(
        OWNER_ID,
        f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>\n\n<code>{message.text}</code>",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

async def ping_cmd(client, message):
    try:
        start = datetime.now()
        await client.invoke(Ping(ping_id=0))
        end = datetime.now()
        uptime = await _human_time_duration((datetime.utcnow() - START_TIME).total_seconds())
        delta_ping = round((end - start).microseconds / 1000, 2)
        await message.reply_text(
            f"<blockquote><b>❏ PONG!!🏓\n"
            f"├• Ping: <code>{delta_ping} ms</code>\n"
            f"├• Uptime: <code>{uptime}</code>\n"
            f"╰• Owners: <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b></blockquote>"
        )
    except UserBannedInChannel:
        pass

async def start_cmd(client, message):
    await add_served_user(message.from_user.id)
    await send_msg_to_owner(client, message)
    if len(message.command) < 2:
        buttons = Button.start(message)
        msg = MSG.START(message)
        await message.reply(msg, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        txt = message.text.split(None, 1)[1]
        msg_id = txt.split("_", 1)[1]
        send = await message.reply("<b>tunggu sebentar...</b>")
        if "secretMsg" in txt:
            try:
                m = [obj for obj in get_objects() if id(obj) == int(msg_id)][0]
            except Exception as error:
                return await send.edit(f"<b>❌ error:</b> <code>{error}</code>")
            user_or_me = [m.reply_to_message.from_user.id, m.from_user.id]
            if message.from_user.id not in user_or_me:
                return await send.edit(
                    f"<b>❌ pesan ini bukan untukmu <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>"
                )
            else:
                text = await client.send_message(
                    message.chat.id,
                    m.text.split(None, 1)[1],
                    protect_content=True,
                    reply_to_message_id=message.id,
                )
                await send.delete()
                await asyncio.sleep(120)
                await message.delete()
                await text.delete()

@DANTE.UBOT("pong")
@DANTE.DEVS("uping")
async def _(client, message):
    await ping_cmd(client, message)

@DANTE.BOT("start")
async def _(client, message):
    await start_cmd(client, message)
