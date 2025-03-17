from DanteUserbot import *
import asyncio
import importlib

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyromod import listen

from pykeyboard import InlineKeyboard
from pyrogram.types import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.raw import functions
from DanteUserbot.core.helpers.unpack import unpackInlineMessage

@DANTE.CALLBACK("cl_ad")
async def cl_ad(client, callback_query):
    """Menampilkan menu bantuan utama."""
    try:
        user_id = callback_query.from_user.id
        if user_id not in getattr(ubot, "_get_my_id", []):  # Pastikan tidak error jika _get_my_id tidak ada
            return
        
        buttons = [
            [InlineKeyboardButton("📖 ǫᴜʀ'ᴀɴ", callback_data="cl_quraan")],
            [
                InlineKeyboardButton("📜 ᴍᴇɴᴜ", callback_data="help_back"),
                InlineKeyboardButton("ℹ️ ɪɴғᴏ", callback_data="cl_info"),
            ],
            [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="cl_close")],
        ]
        await callback_query.edit_message_text(
            "<b>☎️ Menu Bantuan</b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception as e:
        print(f"Error in cl_ad: {e}")

@DANTE.CALLBACK("cl_info")
async def cl_info(client, callback_query):
    """Menampilkan informasi bantuan bot."""
    try:
        user_id = callback_query.from_user.id
        if user_id not in getattr(ubot, "_get_my_id", []):
            return

        buttons = [[InlineKeyboardButton("🔙 ᴋᴇᴍʙᴀʟɪ", callback_data="cl_ad")]]
        
        await callback_query.edit_message_text(
            f"""
<b>☎️ Silakan hubungi: <a href="tg://openmessage?user_id={OWNER_ID}">Admin</a> jika bot mengalami delay atau butuh bantuan.</b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception as e:
        print(f"Error in cl_info: {e}")

@DANTE.CALLBACK("cl_close")
async def cl_close(client, callback_query):
    """Menutup menu bantuan."""
    try:
        user_id = callback_query.from_user.id
        if user_id not in getattr(ubot, "_get_my_id", []):
            return
        
        await callback_query.message.delete()
    except Exception as e:
        print(f"Error in cl_close: {e}")

@DANTE.CALLBACK("cl_quraan")
async def cl_quraan(client, callback_query):
    """Menampilkan menu bantuan untuk perintah Qur'an."""
    try:
        user_id = callback_query.from_user.id
        if user_id not in getattr(ubot, "_get_my_id", []):
            return
        
        buttons = [[InlineKeyboardButton("🔙 ᴋᴇᴍʙᴀʟɪ", callback_data="cl_ad")]]
        
        await callback_query.edit_message_text(
            """
📖 **--Dokumen untuk Qur'an--**

📌 <b>Perintah:</b> `surah [nama surah]`
🔹 <b>Penjelasan:</b> Mengambil informasi Surah.

📌 <b>Perintah:</b> `listsurah`
🔹 <b>Penjelasan:</b> Mendapatkan daftar Surah Al-Quran.
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception as e:
        print(f"Error in cl_quraan: {e}")

@DANTE.CALLBACK("close_user")
async def close_usernya(client, callback_query):
    """Menutup pesan inline yang dikirim oleh bot."""
    try:
        # Gunakan fungsi unpackInlineMessage untuk mendapatkan informasi pesan
        inline_data = unpackInlineMessage(callback_query.inline_message_id)
        if not inline_data:
            return await callback_query.answer("⚠️ Gagal memproses pesan inline!", show_alert=True)

        # Looping ke setiap instance ubot yang sedang berjalan
        for x in getattr(ubot, "_ubot", []):
            if callback_query.from_user.id == int(x.me.id):
                await x.delete_messages(inline_data.chat_id, inline_data.message_id)
    except Exception as e:
        print(f"Error in close_usernya: {e}")
