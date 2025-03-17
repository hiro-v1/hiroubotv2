from HiroUserbot import *

__MODULE__ = "sᴘᴀᴍ"
__HELP__ = f"""
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ꜱᴘᴀᴍ--**

<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}spam</code> [ᴊᴜᴍʟᴀʜ_ᴘᴇꜱᴀɴ - ᴘᴇꜱᴀɴ_ꜱᴘᴀᴍ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ꜱᴘᴀᴍ ᴘᴇꜱᴀɴ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}dspam</code> [ᴊᴜᴍʟᴀʜ_ᴘᴇꜱᴀɴ - ᴊᴜᴍʟᴀʜ_ᴅᴇʟᴀʏ_ᴅᴇᴛɪᴋ - ᴘᴇꜱᴀɴ_ꜱᴘᴀᴍ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ꜱᴘᴀᴍ ᴘᴇꜱᴀɴ ᴅᴇʟᴀʏ
</b></blockquote>  
"""
import asyncio
from gc import get_objects

from pyrogram.enums import ChatType
from pyrogram.errors.exceptions import FloodWait
from HiroUserbot.config import *

async def spam_cmd(client, message):
    reply = message.reply_to_message
    msg = await message.reply("sedang diproses", quote=False)
    if reply:
        try:
            count_message = int(message.command[1])
            for i in range(count_message):
                await reply.copy(message.chat.id)
                await asyncio.sleep(0.1)
        except Exception as error:
            return await msg.edit(str(error))
    else:
        if len(message.command) < 2:
            return await msg.edit(
                "silahkan ketik <code>.help spam</code> untuk melihat cara menggunakan perintah ini"
            )
        else:
            try:
                count_message = int(message.command[1])
                for i in range(count_message):
                    await message.reply(message.text.split(None, 2)[2], quote=False)
                    await asyncio.sleep(0.1)
            except Exception as error:
                return await msg.edit(str(error))
    await msg.delete()
    await message.delete()


async def dspam_cmd(client, message):
    reply = message.reply_to_message
    msg = await message.reply("sedang diproses", quote=False)
    if reply:
        try:
            count_message = int(message.command[1])
            count_delay = int(message.command[2])
        except Exception as error:
            return await msg.edit(str(error))
        for i in range(count_message):
            try:
                await reply.copy(message.chat.id)
                await asyncio.sleep(count_delay)
            except:
                pass
    else:
        if len(message.command) < 4:
            return await msg.edit(
                "silahkan ketik <code>.help spam</code> untuk melihat cara menggunakan perintah ini"
            )
        else:
            try:
                count_message = int(message.command[1])
                count_delay = int(message.command[2])
            except Exception as error:
                return await msg.edit(str(error))
            for i in range(count_message):
                try:
                    await message.reply(message.text.split(None, 3)[3], quote=False)
                    await asyncio.sleep(count_delay)
                except:
                    pass
    await msg.delete()
    await message.delete()

def get_message(message):
    msg = (
        message.reply_to_message
        if message.reply_to_message
        else ""
        if len(message.command) < 2
        else " ".join(message.command[1:])
    )
    return msg


async def get_broadcast_id(client, query):
    chats = []
    chat_types = {
        "group": [ChatType.GROUP, ChatType.SUPERGROUP],
        "users": [ChatType.PRIVATE],
    }
    async for dialog in client.get_dialogs():
        if dialog.chat.type in chat_types[query]:
            chats.append(dialog.chat.id)

    return chats


async def spam_broadcast_cmd(client, message):
    msg = await message.reply("sedang memproses mohon bersabar...")

    send = get_message(message)
    if not send:
        return await msg.edit("mohon balas sesuatu atau ketik sesuatu")

    global broadcast_running
    broadcast_running = True

    chats = await get_broadcast_id(client, "group")
    blacklist = await get_chat(client.me.id)

    done = 0
    failed = 0
    for chat_id in chats:
        if not broadcast_running:
            break

        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue

        try:
            if message.reply_to_message:
                count_message = int(message.command[1])
                for i in range(count_message):
                    await send.copy(chat_id)
                    await asyncio.sleep(0.1)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if message.reply_to_message:
                count_message = int(message.command[1])
                for i in range(count_message):
                    await send.copy(chat_id)
                    await asyncio.sleep(0.1)
            done += 1
        except Exception:
            failed += 1

    return await msg.edit(f"<b>✅ pesan broadcast anda terkirim ke {done} grup. gagal: {failed}</b>")


@HIRO.UBOT("spam|dspam")
async def _(client, message):
    if message.command[0] == "spam":
        await spam_cmd(client, message)
    if message.command[0] == "dspam":
        await dspam_cmd(client, message)

@HIRO.UBOT("spamg")
async def _(client, message):
    if message.command[0] == "spamg":
        await spam_broadcast_cmd(client, message)
