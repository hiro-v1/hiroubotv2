from HiroUserbot import *
import asyncio
import os
from pyrogram.types import Message
from pyrogram import Client
from pyrogram.helpers import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.raw.functions.messages import DeleteHistory

__MODULE__ = "ʜᴀᴘᴜs sᴇᴍᴜᴀ"

__HELP__ = f"""
**--ʜᴀᴘᴜs sᴇᴍᴜᴀ ʙᴏᴛ ᴅᴀɴ ᴄʜᴀᴛ ᴘʀɪʙᴀᴅɪ--**
<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}clearall</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> hapus chat dan bot 
  
  <b>query</b>
  .clearall bot | semua bot yang pernah distart bakal terhapus.
  .clearall semua | semua pesan pribadi kamu dan bot bakal terhapus semua.
  contoh : 
  <b>{PREFIX[0]}clearall semua</b>
</b></blockquote>"""



@HIRO.UBOT("clearall")
async def clearall(client, message):
    rep = message.reply_to_message
    HIROkntl = await message.reply("proses")
    if len(message.command) < 2 and not rep:
        await message.reply("silahkan tunggu")
        return
    if len(message.command) == 1 and rep:
        who = rep.from_user.id
        try:
            info = await client.resolve_peer(who)
            await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
        except PeerIdInvalid:
            pass
        await message.reply("berhasil mengahapus semua chat")
    else:
        if message.command[1].strip().lower() == "all":
            biji = await client.get_chats_dialog("usbot")
            for kelot in biji:
                try:
                    info = await client.resolve_peer(kelot)
                    await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
                except PeerIdInvalid:
                    continue
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    info = await client.resolve_peer(kelot)
                    await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
            await message.reply("sukses menghapus seluruh chat kamu")
        elif message.command[1].strip().lower() == "bot":
            bijo = await client.get_chats_dialog("bot")
            for kelot in bijo:
                try:
                    info = await client.resolve_peer(kelot)
                    await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
                except PeerIdInvalid:
                    continue
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    info = await client.resolve_peer(kelot)
                    await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
            await message.reply("berhasil menghapus semua chat")
        else:
            who = message.text.split(None, 1)[1]
            try:
                info = await client.resolve_peer(who)
                await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
            except PeerIdInvalid:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                info = await client.resolve_peer(who)
                await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
            await message.reply("gagal menghapus chat private kamu")
    return await HIROkntl.delete()
