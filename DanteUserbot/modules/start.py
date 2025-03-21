from .. import *
import asyncio
from datetime import datetime
import sys
from gc import get_objects
from time import time
from DanteUserbot import bot, ubot
from pyrogram.errors.exceptions.bad_request_400 import UserBannedInChannel
from pyrogram.raw.functions import Ping
from pytgcalls import __version__ as pytg
from pyrogram import __version__ as pyr
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from DanteUserbot import *

MODULE = "ᴘɪɴɢ & ꜱᴛᴀʀᴛ"
HELP = f"""--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴘɪɴɢ & ꜱᴛᴀʀᴛ--

<blockquote>
<b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}pong</code>
<b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜᴋᴜʀ ᴋᴇᴄᴇᴘᴀᴛᴀɴ ᴘɪɴɢ ᴅᴀʀɪ ʙᴏᴛ ᴅᴀɴ ᴍᴇɴᴀᴍᴘɪʟᴋᴀɴ ᴜᴘᴛɪᴍᴇ.
</blockquote>

<blockquote>
<b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}start</code>
<b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴᴊᴀʟᴀɴᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ ꜱᴛᴀʀᴛ, ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ ᴋᴇ ᴏᴡɴᴇʀ, ᴅᴀɴ ᴍᴇɴᴇᴍᴘɪʟᴋᴀɴ ʙᴜᴛᴛᴏɴ ꜱᴛᴀʀᴛ.
</blockquote>

"""

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
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else ""))
    return ", ".join(parts)

async def pong(client, message):
    try:
        start = time()
        current_time = datetime.utcnow()
        pong = await message.edit("Proses...")
        delta_ping = time() - start
        await asyncio.sleep(0.3)
        await pong.edit("❏◈===❏")
        await asyncio.sleep(0.3)
        await pong.edit("❏=◈==❏")
        await asyncio.sleep(0.3)
        await pong.edit("❏==◈=❏")
        await asyncio.sleep(0.3)
        await pong.edit("❏===◈❏")
        await asyncio.sleep(0.3)
        await pong.edit("❏==◈=❏")
        await asyncio.sleep(0.3)
        await pong.edit("❏=◈==❏")
        await asyncio.sleep(0.3)
        await pong.edit("❏◈===❏")
        await asyncio.sleep(0.3)
        await pong.edit("❏=◈==❏")
        await asyncio.sleep(0.3)
        await pong.edit("❏==◈=❏")
        await asyncio.sleep(0.3)
        await pong.edit("❏===◈❏")
        await asyncio.sleep(0.3)
        await pong.edit("❏==◈=❏")
        await asyncio.sleep(0.2)
        await pong.edit("❏=◈==❏")
        await asyncio.sleep(0.2)
        await pong.edit("❏◈===❏")
        await asyncio.sleep(0.2)
        await pong.edit("❏=◈==❏")
        await asyncio.sleep(0.2)
        await pong.edit("❏==◈=❏")
        await asyncio.sleep(0.2)
        await pong.edit("❏===◈❏")
        await asyncio.sleep(0.2)
        await pong.edit("❏===◈❏◈")
        await asyncio.sleep(0.2)
        await pong.edit("❏====❏◈◈")
        await asyncio.sleep(0.2)
        await pong.edit("**◈ Pong!**")
        end = datetime.now()
        uptime_sec = (current_time - START_TIME).total_seconds()
        uptime = await _human_time_duration(int(uptime_sec))
        await pong.edit(
            f"<blockquote><b>❏Userbot\n❏Pong : {delta_ping * 1000:.3f} ms\n❏Bot Uptime : {uptime} </b></blockquote>"
        )
    except Exception as error:
        await message.reply(f"Error: {error}")

async def send_msg_to_owner(client, message):
    if message.from_user.id == OWNER_ID:
        return
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    "👤 profil", callback_data=f"profil {message.from_user.id}"
                ),
                InlineKeyboardButton(
                    "jawab 💬", callback_data=f"jawab_pesan {message.from_user.id}"
                ),
            ],
        ]
        await client.send_message(
            OWNER_ID,
            f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>\n\n<code>{message.text}</code>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

from pyrogram.errors.exceptions.bad_request_400 import ReactionInvalid

async def ping_cmd(client, message):
    try:
        start = datetime.now()
        await client.invoke(Ping(ping_id=0))
        end = datetime.now()
        uptime = await get_time((time() - start_time))
        delta_ping = round((end - start).microseconds / 10000, 2)
        _ping = f"""
<blockquote><b>❏ PONG!!🏓
├• Ping: <code>{str(delta_ping).replace('.', ',')} ms</code>
├• Uptime: <code>{uptime}</code>
╰• Owners: <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b></blockquote>
"""
        await message.reply_text(_ping)
    except UserBannedInChannel:
        pass
    except Exception as error:
        await message.reply(f"Error: {error}")

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
        elif "copyMsg" in txt:
            try:
                m = [obj for obj in get_objects() if id(obj) == int(msg_id)][0]
            except Exception as error:
                return await send.edit(f"<b>❌ error:</b> <code>{error}</code>")
            id_copy = int(m.text.split()[1].split("/")[-1])
            if "t.me/c/" in m.text.split()[1]:
                chat = int("-100" + str(m.text.split()[1].split("/")[-2]))
            else:
                chat = str(m.text.split()[1].split("/")[-2])
            try:
                get = await client.get_messages(chat, id_copy)
                await get.copy(message.chat.id, reply_to_message_id=message.id)
                await send.delete()
            except Exception as error:
                await send.edit(error)


@DANTE.UBOT("pong")
@DANTE.DEVS("uping")
async def _(client, message):
    await ping_cmd(client, message)

@DANTE.BOT("start")
async def _(client, message):
    await start_cmd(client, message)

from DanteUserbot import bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@DANTE.BOT("start")
async def start_handler(client, message):
    buttons = [
        [
            InlineKeyboardButton("🎁 Coba Gratis", callback_data="coba_gratis"),
            InlineKeyboardButton("🤖 Buat UBot", callback_data="buat_ubot"),
        ],
        [
            InlineKeyboardButton("📚 Moduls", callback_data="lihat_moduls"),
            InlineKeyboardButton("☎️ Bantuan", callback_data="hubungi_owner"),
        ],
    ]
    await message.reply(
        f"👋 Halo {message.from_user.first_name}!\n\n"
        f"Selamat datang di Hirov2Userbot. Pilih salah satu menu di bawah ini untuk melanjutkan.",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
