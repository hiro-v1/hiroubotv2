from HiroUserbot import *
from pyrogram.raw.functions.messages import DeleteHistory
__MODULE__ = "ᴄʟᴇᴀʀ"
__HELP__ = f"""
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄʟᴇᴀʀ--**
<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}clear</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜs ʜɪsᴛᴏʀʏ</b></blockquote>
"""


@HIRO.UBOT("clear")
async def _(client, message):
    user_id = message.chat.id
    bot_info = await client.resolve_peer(user_id)
    await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))
