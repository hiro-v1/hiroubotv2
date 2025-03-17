__MODULE__ = "ʀᴇᴀᴄᴛ"
__HELP__ = """
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʀᴇᴀᴄᴛɪᴏɴ--**

<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}ʀᴇᴀᴄᴛ</code></code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴇʀɪᴋᴀɴ ʀᴇᴀᴄᴛɪᴏɴ ᴋᴇ ꜱᴇʟᴜʀᴜʜ ᴄʜᴀᴛ ʏᴀɴɢ ᴀɴᴅᴀ ɪɴɢɪɴᴋᴀɴ.
  
  
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}ꜱᴛᴏᴘʀᴇᴀᴄᴛ</code></code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴇɴᴛɪᴋᴀɴ ʀᴇᴀᴄᴛɪᴏɴ.

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}ꜱᴠᴋᴏɴ</code></code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴʏɪᴍᴘᴀɴ ᴋᴏɴᴛᴀᴋ ᴘᴇɴɢɢᴜɴᴀ
</b></blockquote>
"""

from DanteUserbot import *
from pyrogram import Client, idle, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.types import ChatMember
from pyrogram.errors.exceptions import UserNotParticipant

reaction_progress = False

@DANTE.UBOT("react")
async def _(c, m):
    global reaction_progress
    reaction_progress = True
    try:
        if len(m.command) != 3:
            await m.reply("Mohon gunakan format: react username/id emoji")
            return

        chat_id = m.command[1]
    except IndexError:
        await m.reply("Mohon gunakan format: react username/id emoji")
        return

    rach = await m.reply("Processing..")
    async for message in c.get_chat_history(chat_id):
        await asyncio.sleep(0.5)
        chat_id = message.chat.id
        message_id = message.id
        try:
            if not reaction_progress:
                break
            await asyncio.sleep(0.5)
            await c.send_reaction(chat_id=chat_id, message_id=message_id, emoji=m.command[2])
        except Exception:
            pass
    
    await rach.edit(f"**Reaction telah selesai **✅")


@DANTE.UBOT("stopreact")
async def _(client, message):
    global reaction_progress
    reaction_progress = False
    await message.reply("Proses reaction telah dibatalkan.")
