from HiroUserbot import *
from HiroUserbot.core.database.saved import get_chat
from pyrogram import Client
from pyrogram import errors
from pyrogram import enums
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate


__MODULE__ = "ɢᴀʙᴜɴɢ"
__HELP__ = f"""<blockquote><b>
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴊᴏɪɴʟᴇᴀᴠᴇ 』</b>

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}kickme</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ ɢʀᴜᴘ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}join</code> [ᴜꜱᴇʀɴᴀᴍᴇɢᴄ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴊᴏɪɴ ᴋᴇ ɢʀᴜᴘ ᴍᴇʟᴀʟᴜɪ ᴜꜱᴇʀɴᴀᴍᴇ 

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}leaveallgc</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ ꜱᴇᴍᴜᴀ ɢʀᴜᴘ ʏᴀɴɢ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ/ᴏᴡɴᴇʀ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}leaveallmute</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ ꜱᴇᴍᴜᴀ ɢʀᴜᴘ ʏᴀɴɢ ᴍᴇᴍʙᴀᴛᴀꜱɪ ᴀɴᴅᴀ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}leaveallch</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ ꜱᴇᴍᴜᴀ ᴄʜᴀɴɴᴇʟ ʏᴀɴɢ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ/ᴏᴡɴᴇʀ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}leave</code> [ᴜꜱᴇʀɴᴀᴍᴇɢᴄ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ ɢʀᴜᴘ ᴍᴇʟᴀʟᴜɪ ᴜꜱᴇʀɴᴀᴍᴇ
</b></blockquote>"""
from pyrogram import Client, enums, filters
from pyrogram.types import Message
import asyncio
from HiroUserbot.core.database.saved import get_chat
from pyrogram.enums import ChatType, ChatMemberStatus
from HiroUserbot.core.function.emoji import emoji

from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant


@HIRO.UBOT("kickme|leave")
async def leave(client: Client, message: Message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply(f"<b>{prs}sedang ᴍᴇᴍᴘʀᴏꜱᴇꜱ<b>...")
    if message.chat.id in BLACKLIST_CHAT:
        return await xxnx.edit(f"<b>{ggl}perintah ini dilarang digunakan di group ini</b>")
    try:
        await xxnx.edit_text(f"{client.me.first_name} <b>{sks}telah meninggalkan grup ini, bye!!<b>")
        await client.leave_chat(Man)
    except Exception as ex:
        await xxnx.edit_text(f"{ggl}ERROR: \n\n{str(ex)}")


@HIRO.UBOT("join")
async def join(client: Client, message: Message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply(f"<b>ᴍᴇᴍᴘʀᴏꜱᴇꜱ...</b>")
    try:
        await xxnx.edit(f"<b>{sks}berhaꜱil bergabung ke chat id</b> `{Man}`")
        await client.join_chat(Man)
    except Exception as ex:
        await xxnx.edit(f"{ggl}ERROR: \n\n{str(ex)}")


@HIRO.UBOT("leaveallgc")
async def _(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    done = 0
    Haku = await message.reply(f"{prs}<b>proccesing...</b>")
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
            chat_id = dialog.chat.id
            await asyncio.sleep(0.1)
            try:
                member = await client.get_chat_member(chat_id, "me")
                if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                    done += 1
                    await client.leave_chat(chat_id)
            except Exception:
                pass
    await Haku.edit(f"<b>{sks}berhasil keluar dari {done} grup yang bukan admin/owner</b>")

@HIRO.UBOT("leaveallmute")
async def _(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    done = 0
    Haku = await message.reply(f"<b>{prs}Proccesing...</b>")
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
            chat_id = dialog.chat.id
            try:
                member = await client.get_chat_member(chat_id, "me")
                if member.status == ChatMemberStatus.RESTRICTED:
                    await client.leave_chat(chat_id)
                    done += 1
            except Exception:
                pass
    await Haku.edit(f"<b>{sks}berhasil keluar dari {done} grup yang membatasi anda<b>")


@HIRO.UBOT("leaveallch")
async def kickmeallch(client: Client, message: Message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    Man = await message.reply(f"<b>{prs}global leave dari channel<b>...")
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.CHANNEL:
            chat = dialog.chat.id
            member = await client.get_chat_member(chat, "me")
            if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                try:
                    await client.leave_chat(chat)
                    done += 1
                except Exception:
                    pass
    await Man.edit(f"<b>{sks}berhasil keluar dari {done}<b>")
