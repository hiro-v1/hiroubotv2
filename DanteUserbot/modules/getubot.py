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
    msg = await message.reply("**tunggu sebentar**..", quote=True)
    try:
        x = await client.get_inline_bot_results(bot.me.username, "ambil_ubot")
        await message.reply_inline_bot_result(x.query_id, x.results[0].id, quote=True)
        await msg.delete()
    except Exception as error:
        await msg.edit(f"⚠️ Terjadi kesalahan:\n<code>{error}</code>")

@DANTE.INLINE("^ambil_ubot")
async def getubot_query(client, inline_query):
    msg = await MSG.USERBOT(0)  # Ambil pesan userbot dari fungsi MSG
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            InlineQueryResultArticle(
                title="💬",
                reply_markup=InlineKeyboardMarkup(Button.ambil_akun(ubot._ubot[0].me.id, 0)),
                input_message_content=InputTextMessageContent(msg),
            )
        ],
    )
