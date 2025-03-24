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
    if message.from_user.id != OWNER_ID:
        await send_msg_to_owner(client, message)

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
    welcome_text = (
        f"👋 Halo {message.from_user.first_name}!\n\n"
        f"Selamat datang di HiroUserbot. HiroUserbot adalah solusi otomatisasi Telegram yang andal dan mudah digunakan.\n\n"
        f"Pilih salah satu menu di bawah ini untuk melanjutkan."
    )
    await message.reply(welcome_text, reply_markup=InlineKeyboardMarkup(buttons))

@DANTE.UBOT("pong")
@DANTE.DEVS("uping")
async def _(client, message):
    await ping_cmd(client, message)

@DANTE.BOT("start")
async def _(client, message):
    await start_cmd(client, message)

@DANTE.CALLBACK("profil")
async def profil_callback(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    user = await client.get_users(user_id)
    full_name = f"{user.first_name} {user.last_name or ''}"
    username = f"@{user.username}" if user.username else "Tidak ada username"
    profile_text = (
        f"👤 <b>Profil Pengguna:</b>\n"
        f"📌 <b>Nama:</b> {full_name}\n"
        f"🔗 <b>Username:</b> {username}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>"
    )
    await callback_query.message.edit_text(profile_text)

@DANTE.CALLBACK("jawab_pesan")
async def jawab_pesan_callback(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    await callback_query.message.reply(f"Silakan balas pesan ini untuk mengirim pesan ke pengguna dengan ID {user_id}.")

async def lihat_moduls_callback(client, callback_query):
    SH = await ubot.get_prefix(callback_query.from_user.id)
    top_text = f"<b>❏ Moduls\n├ Prefixes: {' '.join(SH)}\n╰ Commands: {len(HELP_COMMANDS)}</b>"
    await callback_query.message.edit_text(
        text=top_text,
        reply_markup=InlineKeyboardMarkup(
            paginate_modules(0, HELP_COMMANDS, "help")
        ),
        disable_web_page_preview=True,
    )

@DANTE.CALLBACK("hubungi_owner")
async def hubungi_owner_callback(client, callback_query):
    await callback_query.message.edit_text(
        f"☎️ Jika Anda membutuhkan bantuan, silakan hubungi owner: <a href='tg://user?id={OWNER_ID}'>Klik di sini</a>.",
        disable_web_page_preview=True,
    )

@DANTE.CALLBACK("coba_gratis")
async def coba_gratis_callback(client, callback_query):
    user_id = callback_query.from_user.id
    if await is_trial_used(user_id):
        await callback_query.answer("❌ Anda sudah pernah mencoba gratis.", show_alert=True)
        return
    now = datetime.now()
    expired_date = now + timedelta(days=1)
    await add_prem(user_id)
    await set_expired_date(user_id, expired_date)
    await mark_trial_used(user_id)
    await callback_query.message.edit_text("✅ Anda telah mendapatkan akses premium selama 1 hari!")

@DANTE.CALLBACK("buat_ubot")
async def buat_ubot_callback(client, callback_query):
    # Arahkan ke payment_userbot untuk memeriksa status pembayaran
    await payment_userbot(client, callback_query)

@DANTE.BOT("start")
async def start_handler(client, message):
    await start_cmd(client, message)

@DANTE.CALLBACK("lihat_moduls")
async def lihat_moduls_callback(client, callback_query):
    """Handles the 'lihat_moduls' callback query."""
    SH = await ubot.get_prefix(callback_query.from_user.id)
    top_text = f"<b>❏ Moduls\n├ Prefixes: {' '.join(SH)}\n╰ Commands: {len(HELP_COMMANDS)}</b>"
    await callback_query.message.edit_text(
        text=top_text,
        reply_markup=InlineKeyboardMarkup(
            paginate_modules(0, HELP_COMMANDS, "help")
        ),
        disable_web_page_preview=True,
    )
