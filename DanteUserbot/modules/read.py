from DanteUserbot import *

__MODULE__ = "ʙᴀᴄᴀ"

__HELP__ = f"""
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʙᴀᴄᴀ--**

<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ʙᴀᴄᴀ</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴄᴀ ꜱᴇᴍᴜᴀ ᴘᴇꜱᴀɴ ʏᴀɴɢ ʙᴇʟᴜᴍ ᴛᴇʀʙᴀᴄᴀ
</b></blockquote>"""

from pyrogram import Client, idle, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.types import ChatMember
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.errors.exceptions import UserNotParticipant

@DANTE.UBOT("baca")
async def baca_read(client, message):
    Mai = await message.reply_text(f"Proccesing...")
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.PRIVATE:
            user_id = dialog.chat.id
            anjai = await client.read_chat_history(user_id)
            if anjai:
                done += 1
    await Mai.edit_text(f"Berhasil Membaca Pesan Dari : {done} User✅")

