__MODULE__ = "ᴀʙsᴇɴ"
__HELP__ = """
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴀʙꜱᴇɴ--**
<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}absen</code>
  <b>• ᴇxᴘʟᴀɴᴀsɪ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ʟɪꜱᴛ ᴀʙꜱᴇɴ.</b></blockquote> 
<blockquote><b>  
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}delabsen</code>
  <b>• ᴇxᴘʟᴀɴᴀsɪ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜs ʟɪꜱᴛ ᴀʙꜱᴇɴ.</b></blockquote>"""

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup, InlineQueryResultArticle, 
    InputTextMessageContent, InlineKeyboardButton
)
from datetime import datetime
import pytz
import asyncio

from DanteUserbot import *
from DanteUserbot.core.function.emoji import EMO
from DanteUserbot.core.helpers.client import *

# Daftar yang hadir
hadir_list = []

# Fungsi untuk mendapatkan daftar absen
def get_hadir_list():
    if not hadir_list:
        return "📌 ʙᴇʟᴜᴍ ᴀᴅᴀ ʏᴀɴɢ ʜᴀᴅɪʀ"
    return "\n".join([f"👤 {user['mention']} - {user['jam']}" for user in hadir_list])

# Perintah Absen
@DANTE.UBOT("absen")
async def absen_command(c, m):
    ggl = await EMO.GAGAL(c)
    prs = await EMO.PROSES(c)

    user_id = m.from_user.id
    mention = m.from_user.mention
    jam = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")

    hadir_list.append({"user_id": user_id, "mention": mention, "jam": jam})
    
    try:
        x = await c.get_inline_bot_results(c.me.username, "absen_in")
        if x.results:
            await m.reply_inline_bot_result(x.query_id, x.results[0].id)
        else:
            await m.reply(f"{ggl} **ᴛɪᴅᴀᴋ ᴀᴅᴀ ʜᴀsɪʟ ɪɴʟɪɴᴇ ʙᴏᴛ.**")
    except asyncio.TimeoutError:
        await m.reply(f"{ggl} **ᴡᴀᴋᴛᴜ ʜᴀʙɪs ᴅᴀʟᴀᴍ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ʜᴀsɪʟ ɪɴʟɪɴᴇ ʙᴏᴛ.**")
    except Exception as e:
        await m.reply(f"{ggl} **ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ:** `{e}`")

# Perintah Menghapus Absen
@DANTE.UBOT("delabsen")
async def clear_absen_command(c, m):
    hadir_list.clear()
    sks = await EMO.BERHASIL(c)
    await m.reply(f"{sks} **sᴇᴍᴜᴀ ᴀʙsᴇɴ ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs.**")

# Menangani Query Inline untuk Absen
@DANTE.INLINE("absen_in")
async def absen_query(c, iq):
    user_id = iq.from_user.id
    mention = iq.from_user.mention
    jam = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")

    hadir_list.append({"user_id": user_id, "mention": mention, "jam": jam})
    hadir_text = get_hadir_list()

    text = f"**📅 ᴀʙsᴇɴ ᴛᴀɴɢɢᴀʟ:**\n{datetime.now().strftime('%d-%m-%Y')}\n\n**👥 ʟɪsᴛ ᴀʙsᴇɴ:**\n{hadir_text}\n"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✅ ʜᴀᴅɪʀ", callback_data="absen_hadir")]])

    await c.answer_inline_query(
        iq.id,
        results=[
            InlineQueryResultArticle(
                title="📌 ᴀʙsᴇɴ",
                input_message_content=InputTextMessageContent(text),
                reply_markup=keyboard
            )
        ],
    )

# Menangani Callback untuk Hadir
@DANTE.CALLBACK("absen_hadir")
async def hadir_callback(c, cq):
    user_id = cq.from_user.id
    mention = cq.from_user.mention
    jam = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")

    if any(user['user_id'] == user_id for user in hadir_list):
        await cq.answer("❌ Anda sudah absen sebelumnya!", show_alert=True)
        return

    hadir_list.append({"user_id": user_id, "mention": mention, "jam": jam})
    hadir_text = get_hadir_list()

    text = f"**📅 ᴀʙsᴇɴ ᴛᴀɴɢɢᴀʟ:**\n{datetime.now().strftime('%d-%m-%Y')}\n\n**👥 ʟɪsᴛ ᴀʙsᴇɴ:**\n{hadir_text}\n"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✅ ʜᴀᴅɪʀ", callback_data="absen_hadir")]])

    await cq.edit_message_text(text, reply_markup=keyboard)
