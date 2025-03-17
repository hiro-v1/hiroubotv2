from DanteUserbot import *
import asyncio
import os

from gc import get_objects
from time import time
from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import *
from DanteUserbot.core.helpers.emoji import EMO
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle, InputTextMessageContent)


__MODULE__ = "ᴄᴏᴘʏ"
__HELP__ = f"""
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄᴏᴘʏ--**

<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ᴄᴏᴘʏ</code> [ʟɪɴᴋ_ᴋᴏɴᴛᴇɴ_ᴛᴇʟᴇɢʀᴀᴍ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴍʙɪʟ ᴘᴇsᴀɴ ᴅᴀɴ ᴘᴏsᴛɪɴɢᴀɴ ᴄʜᴀɴᴇʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇʟᴀʟᴜɪ ʟɪɴᴋ ᴍᴇʀᴇᴋᴀ
 </b></blockquote> """

async def nyolongnih(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    try:
        await message.edit(f"{prs}<b>ᴘʀᴏᴄᴄᴇsɪɴɢ</b>...")
        link = get_arg(message)
        msg_id = int(link.split("/")[-1])
        if "t.me/c/" in link:
            try:
                chat = int("-100" + str(link.split("/")[-2]))
                dia = await client.get_messages(chat, msg_id)
            except RPCError:
                return await message.edit(f"{ggl}**sᴇᴘᴇʀᴛɪɴʏᴀ ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ**")
        else:
            try:
                chat = str(link.split("/")[-2])
                dia = await client.get_messages(chat, msg_id)
            except RPCError:
                return await message.edit(f"{ggl}**sᴇᴘᴇʀᴛɪɴʏᴀ ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ**")
        
        anjing = dia.caption or None
        if dia.text:
            await dia.copy(message.chat.id)
            await message.delete()
        elif dia.photo:
            anu = await client.download_media(dia)
            await client.send_photo(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        elif dia.video:
            anu = await client.download_media(dia)
            await client.send_video(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        elif dia.audio:
            anu = await client.download_media(dia)
            await client.send_audio(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        elif dia.voice:
            anu = await client.download_media(dia)
            await client.send_voice(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        elif dia.document:
            anu = await client.download_media(dia)
            await client.send_document(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        else:
            await message.edit(f"{ggl}**sᴇᴘᴇʀᴛɪɴʏᴀ ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ**")
    except Exception as e:
        await message.reply_text(str(e))

@DANTE.UBOT("copy")
async def _(client, message):
    await nyolongnih(client, message)
