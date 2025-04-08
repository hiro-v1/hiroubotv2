from DanteUserbot import *
import importlib
import random
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

from DanteUserbot.core.helpers import Ubot, loadModule, set_expired_date, add_ubot, get_DanteUserbots
from DanteUserbot.core.helpers.client import DANTE, FILTERS
from DanteUserbot.core.function.plugins import loadPlugins

@DANTE.BOT("login", FILTERS.OWNER)
@DANTE.UBOT("login")
@DANTE.OWNER
async def login_userbot(client, message):
    info = await message.reply("<b>tunggu sebentar...</b>", quote=True)
    if len(message.command) < 3:
        return await info.edit(
            f"<code>{message.text}</code> <b>hari - string pyrogram</b>"
        )
    try:
        ub = Ubot(
            name=f"ubot_{random.randrange(999999)}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=message.command[2],
        )
        await ub.start()
        for mod in loadModule():
            importlib.reload(importlib.import_module(f"DanteUserbot.modules.{mod}"))
        now = datetime.now(timezone("Asia/Jakarta"))
        expire_date = now + timedelta(days=int(message.command[1]))
        await set_expired_date(ub.me.id, expire_date)
        await add_ubot(
            user_id=int(ub.me.id),
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=message.command[2],  # Fix parameter session_string
        )
        buttons = [
            [
                InlineKeyboardButton(
                    "📁 cek masa aktif 📁",
                    callback_data=f"cek_masa_aktif {ub.me.id}",
                )
            ],
        ]
        await bot.send_message(
            LOGS_MAKER_UBOT,
            f"""
<b>❏ userbot diaktifkan</b>
<b> ├ akun:</b> <a href=tg://user?id={ub.me.id}>{ub.me.first_name} {ub.me.last_name or ''}</a> 
<b> ╰ id:</b> <code>{ub.me.id}</code>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
        return await info.edit(
            f"<b>✅ berhasil login di akun: <a href='tg://user?id={ub.me.id}'>{ub.me.first_name} {ub.me.last_name or ''}</a></b>"
        )
    except Exception as error:
        return await info.edit(f"<code>{error}</code>")

@DANTE.BOT("restart")
async def restart_userbot(client, message):
    msg = await message.reply("<b>tunggu sebentar...</b>", quote=True)
    if message.from_user.id not in ubot._get_my_id:
        return await msg.edit(
            f"<b>Anda tidak bisa menggunakan perintah ini karena Anda bukan pengguna @{bot.me.username}</b>"
        )
    for X in ubot._ubot:
        if message.from_user.id == X.me.id:
            for _ubot_ in await get_DanteUserbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        ubot._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        await loadPlugins()  # Memuat ulang modul dan mengirim pesan
                        return await msg.edit(
                            f"<b>✅ Restart berhasil dilakukan untuk {UB.me.first_name} {UB.me.last_name or ''} | {UB.me.id}</b>"
                        )
                    except Exception as error:
                        return await msg.edit(f"<b>{error}</b>")

@DANTE.CALLBACK("cek_masa_aktif")
async def cek_masa_aktif_callback(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired_date = await get_expired_date(user_id)
    if expired_date:
        remaining_days = (expired_date - datetime.now(timezone("Asia/Jakarta"))).days
        await callback_query.answer(f"⏳ Masa aktif tersisa: {remaining_days} hari.", show_alert=True)
    else:
        await callback_query.answer("✅ Userbot sudah tidak aktif.", show_alert=True)

@DANTE.CALLBACK("restart_all")
async def restart_all_userbots(client, callback_query):
    """Restart semua userbot yang sedang berjalan."""
    await callback_query.answer("⏳ Memulai ulang semua userbot...", show_alert=True)
    for X in ubot._ubot:
        try:
            ubot._ubot.remove(X)
            ubot._get_my_id.remove(X.me.id)
            await X.stop()
            await X.start()
        except Exception as error:
            print(f"⚠️ Gagal restart userbot {X.me.id}: {error}")
    await callback_query.message.edit_text("✅ Semua userbot berhasil di-restart.")
