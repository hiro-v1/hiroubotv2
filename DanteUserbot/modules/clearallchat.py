from DanteUserbot import *
import asyncio
import os
from pyrogram.types import Message
from pyrogram import Client
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
</b></blockquote>

**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄʟᴇᴀʀ--**
<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}clear</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜs ʜɪsᴛᴏʀʏ</b></blockquote>
"""

@DANTE.UBOT("clearall")
async def clearall(client, message):
    rep = message.reply_to_message
    dantekntl = await message.reply("proses")
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
        if message.command[1].strip().lower() == "semua":
            biji = await client.get_dialogs()
            for kelot in biji:
                try:
                    info = await client.resolve_peer(kelot.chat.id)
                    await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
                except PeerIdInvalid:
                    continue
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    info = await client.resolve_peer(kelot.chat.id)
                    await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
            await message.reply("sukses menghapus seluruh chat kamu")
        elif message.command[1].strip().lower() == "bot":
            bijo = await client.get_dialogs()
            for kelot in bijo:
                if kelot.chat.type == ChatType.BOT:
                    try:
                        info = await client.resolve_peer(kelot.chat.id)
                        await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
                    except PeerIdInvalid:
                        continue
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        info = await client.resolve_peer(kelot.chat.id)
                        await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
            await message.reply("berhasil menghapus semua chat bot")
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
    return await dantekntl.delete()

@DANTE.UBOT("clear")
async def clear(client, message):
    user_id = message.chat.id
    bot_info = await client.resolve_peer(user_id)
    await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))
    await message.reply("berhasil menghapus history chat")
