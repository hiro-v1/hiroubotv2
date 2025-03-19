from DanteUserbot import *

__MODULE__ = "sᴇᴄʀᴇᴛ"
__HELP__ = f"""
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ꜱᴇᴄʀᴇᴛ--**

<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}msg</code> [ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ - ᴛᴇxᴛ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ ꜱᴇᴄᴀʀᴀ ʀᴀʜᴀꜱɪᴀ
</b></blockquote>"""
from gc import get_objects

from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle, InputTextMessageContent)

# Ensure bot object is defined or imported
from DanteUserbot import bot

@DANTE.UBOT("msg")
async def _(client, message):
    if not message.reply_to_message:
        return await message.reply(
            f"<code>{message.text}</code> [reply to user - text]"
        )
    text = f"secret {id(message)}"
    await message.delete()
    x = await client.get_inline_bot_results(bot.me.username, text)
    await message.reply_to_message.reply_inline_bot_result(x.query_id, x.results[0].id)

@DANTE.INLINE("^secret")
async def _(client, q):
    try:
        m = [obj for obj in get_objects() if id(obj) == int(q.query.split()[1])][0]
    except IndexError:
        return await client.answer_inline_query(
            q.id,
            cache_time=0,
            results=[]
        )
    await client.answer_inline_query(
        q.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="pesan rahasia!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="💬 baca pesan rahasia 💬",
                                    url=f"https://t.me/{bot.me.username}?start=secretMsg_{int(q.query.split(None, 1)[1])}",
                                )
                            ],
                        ]
                    ),
                    input_message_content=InputTextMessageContent(
                        f"<b>👉🏻 ada pesan rahasia untuk mu nih:</b> <a href='tg://user?id={m.reply_to_message.from_user.id}'>{m.reply_to_message.from_user.first_name} {m.reply_to_message.from_user.last_name or ''}</a>"
                    ),
                )
            )
        ],
    )

