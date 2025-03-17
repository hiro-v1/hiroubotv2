from DanteUserbot import *
import asyncio
import os
from pyrogram.types import Message
from pyrogram import Client
from pyrogram.helpers import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.raw.functions.messages import DeleteHistory

__MODULE__ = "ᴄʟᴇᴀʀ ᴄʜᴀᴛ²"

__HELP__ = f"""
**--ᴄʟᴇᴀʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ--**
<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}cc</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> hapus chat digroup replay ke users atau diri
  note : kamu harus admin digroup | semua chat kamu bakal terhapus.
</b></blockquote>"""

      
@DANTE.UBOT("cc")
async def cc(client, message):
    reply = message.reply_to_message
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        aan = await message.reply("proses..")
        await asyncio.sleep(0.3)
        return await aan.delete()
    
    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        aa = await message.reply("silahkan tunggu..")
        await asyncio.sleep(0.3)
        return await aa.delete()
    
    await message.delete()
    try:
        await client.delete_user_history(message.chat.id, user)
        await message.reply("berhasil menghapus semua pesan pengguna.")
    except Exception as ev:
        print(f"Error saat menghapus pesan: {ev}")
        await message.reply("gagal menghapus pesan pengguna.")     
