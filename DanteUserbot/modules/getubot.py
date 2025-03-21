from DanteUserbot import *
import random
from datetime import datetime
from time import time
from DanteUserbot.core.function.emoji import emoji
from pyrogram.raw.functions import Ping
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
)
from DanteUserbot.core.helpers.client import DANTE

@DANTE.UBOT("getubot")
@DANTE.OWNER
async def getubot_cmd(client, message):
    """Mengambil akun userbot melalui inline mode."""
    msg = await message.reply("⏳ Tunggu sebentar...", quote=True)

    if not bot.me.username:
        return await msg.edit("❌ Bot tidak memiliki username. Aktifkan inline mode!")

    try:
        x = await client.get_inline_bot_results(bot.me.username, "ambil_ubot")
        if not x.results:
            return await msg.edit("❌ Tidak ada hasil yang ditemukan.")

        await message.reply_inline_bot_result(
            x.query_id,
            x.results[0].id,
            quote=True,
        )
        await msg.delete()

    except Exception as error:
        await msg.edit(f"⚠️ Terjadi kesalahan:\n<code>{error}</code>")

@DANTE.INLINE("^ambil_ubot")
async def getubot_query(client, inline_query):
    """Menampilkan inline query untuk mengambil akun userbot."""
    try:
        msg = "💬 Ambil akun userbot."
        userbot_id = ubot._ubot[0].me.id if ubot._ubot else 0

        buttons = [
            [
                InlineKeyboardButton("🔙 Kembali", callback_data="start"),
                InlineKeyboardButton("❌ Tutup", callback_data="cl_close"),
            ]
        ]

        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                InlineQueryResultArticle(
                    title="💬 Ambil Akun",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    input_message_content=InputTextMessageContent(msg),
                )
            ],
        )

    except Exception as error:
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[],
            switch_pm_text=f"⚠️ Error: {error}",
            switch_pm_parameter="error",
        )
