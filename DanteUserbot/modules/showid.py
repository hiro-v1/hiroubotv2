from DanteUserbot import *
from pyrogram.enums import ParseMode

__MODULE__ = "ᴄᴇᴋ ɪᴅ"
__HELP__ = f"""
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ꜱʜᴏᴡɪᴅ--**

<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}id</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ɪᴅ ᴅᴀʀɪ ᴜꜱᴇʀ/ɢʀᴜᴘ/ᴄʜᴀɴɴᴇʟ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}id</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ɪᴅ ᴅᴀʀɪ ᴇᴍᴏᴊɪ ᴘʀᴇᴍ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}id</code> [ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ/ᴍᴇᴅɪᴀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ɪᴅ ᴅᴀʀɪ ᴜꜱᴇʀ/ᴍᴇᴅɪᴀ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}id</code> [ᴜꜱᴇʀɴᴀᴍᴇ ᴜꜱᴇʀ/ɢʀᴜᴘ/ᴄʜᴀɴɴᴇʟ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ɪᴅ ᴜꜱᴇʀ/ɢʀᴜᴘ/ᴄʜᴀɴɴᴇʟ ᴍᴇʟᴀʟᴜɪ ᴜꜱᴇʀɴᴀᴍᴇ
</b></blockquote>"""
import html
import asyncio
from pyrogram import *
from pyrogram.raw.types import *
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram import filters

import logging

from pyrogram.enums import ChatType


@DANTE.UBOT("id")
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"{sks}**[Message ID:]({message.link})** `{message_id}`\n"
    text += f"{sks}**[Your ID:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()
        
    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"{sks}**[User ID:](tg://user?id={user_id})** `{user_id}`\n"

        except Exception:
            return await message.edit_text("This user doesn't exist.", quote=True)

    text += f"{sks}**[Chat ID:](https://t.me/{chat.username})** `{chat.id}`\n\n"

    if not getattr(reply, "empty", True) and not message.forward_from_chat and not reply.sender_chat:
        text += (
            f"{sks}**[Replied Message ID:]({reply.link})** `{message.reply_to_message.id}`\n"
        )
        text += f"{sks}**[Replied User ID:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"The forwarded channel, {reply.forward_from_chat.title}, has an id of `{reply.forward_from_chat.id}`\n\n"
        print(reply.forward_from_chat)
    
    if reply and reply.sender_chat:
        text += f"ID of the replied chat/channel, is `{reply.sender_chat.id}`"
        print(reply.sender_chat)

    await message.edit_text(
       text,
       disable_web_page_preview=True,
    )

@DANTE.UBOT("idm")
async def _(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    zeb = message.reply_to_message
    if not zeb:
        return await message.reply_text("{ggl}<b>ᴍᴏʜᴏɴ ʙᴀʟᴀs ᴋᴇ ᴇᴍᴏᴊɪ ᴘʀᴇᴍɪᴜᴍ!</b>")
    try:
        emoji_text = zeb.text
        emoji_id = zeb.entities[0].custom_emoji_id
        await message.reply_text(f"`<emoji id={emoji_id}>{emoji_text}</emoji>`", parse_mode=ParseMode.MARKDOWN)
    except NoneType:
        await message.reply_text("{ggl}<b>ᴍᴏʜᴏɴ ʙᴀʟᴀs ᴋᴇ ᴇᴍᴏᴊɪ ᴘʀᴇᴍɪᴜᴍ!</b>")
