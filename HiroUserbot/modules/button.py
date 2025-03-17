from HiroUserbot import *
import asyncio
import importlib

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyromod import listen

from pykeyboard import InlineKeyboard
from pyrogram.types import *
from pyrogram.raw import functions


@HIRO.CALLBACK("cl_ad")
async def cl_ad(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [
                InlineKeyboardButton("ǫᴜʀ'ᴀɴ", callback_data="cl_quraan"),
            ],
            [
                InlineKeyboardButton("ᴍᴇɴᴜ", callback_data="help_back"),
                InlineKeyboardButton("ɪɴғᴏ", callback_data="cl_info")
            ],
            [
                InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="cl_close")
            ],
        ]
        return await callback_query.edit_message_text(
            f"""
<b>☎️ Menu Bantuan</b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        
@HIRO.CALLBACK("cl_info")
async def cl_info(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [
                InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data="cl_ad")
            ],
        ]        
        return await callback_query.edit_message_text(
            f"""
<b>☎️ silahkan hubungi: <a href=tg://openmessage?user_id={OWNER_ID}>admin</a> jika bot kamu delay atau butuh bantuan mengenai bot</b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        
@HIRO.CALLBACK("cl_close")       
async def cl_close(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        return await callback_query.edit_message_text(
            f"""
⚠️ Menu Ditutup!</b>
""",
            disable_web_page_preview=True,
        )

@HIRO.CALLBACK("cl_quraan")
async def cl_quraan(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [
                InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data="cl_ad")
            ],
        ]        
        return await callback_query.edit_message_text(
            f"""
  🗂️ **--Dokumen untuk Qur'an--**
  
  <blockquote><b>📚 Perintah:</b> `surah [nama surah]`
  <b>👉 Keterangan:</b> Mengambil informasi Surah.</blockquote>
  <blockquote><b>📚 Perintah:</b> `listsurah`
  <b>👉 Keterangan:</b> Mendapatkan Daftar Surah Al-Quran.</blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )

@HIRO.CALLBACK("close_user")
async def close_usernya(client, callback_query):
    unPacked = unpackInlineMessage(callback_query.inline_message_id)
    for x in ubot._ubot:
        if callback_query.from_user.id == int(x.me.id):
            await x.delete_messages(
                unPacked.chat_id, unPacked.message_id
            )
