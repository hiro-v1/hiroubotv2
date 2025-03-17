from DanteUserbot import *

__MODULE__ = "sᴏsᴍᴇᴅ"
__HELP__ = f"""
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ꜱᴏꜱᴍᴇᴅ--**

<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ꜱᴏꜱᴍᴇᴅ</code> [ʟɪɴᴋ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴏᴡɴʟᴏᴀᴅ ᴍᴇᴅɪᴀ ᴅᴀʀɪ ꜰᴀᴄᴇʙᴏᴏᴋ/ᴛɪᴋᴛᴏᴋ/ɪɴꜱᴛᴀɢʀᴀᴍ/ᴛᴡɪᴛᴛᴇʀ/ʏᴏᴜᴛᴜʙᴇ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ꜱᴏɴɢ</code> [ꜱᴏɴɢ ᴛɪᴛʟᴇ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b>  ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴏᴡɴʟᴏᴀᴅ ᴍᴜꜱɪᴄ ʏᴀɴɢ ᴅɪɪɴɢɪɴᴋᴀɴ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ᴠꜱᴏɴɢ</code> [ꜱᴏɴɢ ᴛɪᴛʟᴇ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ ʏᴀɴɢ ᴅɪɪɴɢɪɴᴋᴀɴ
</b></blockquote>"""

import asyncio
from pyrogram.raw.functions.messages import DeleteHistory

@DANTE.UBOT("sosmed")
async def download_media(client, message):
    """
    Command to download media from various social media platforms.
    """
    if len(message.command) < 2:
        return await message.reply(
            f"<code>{message.text}</code> link yt/ig/fb/tw/tiktok"
        )
    else:
        bot_username = "thisvidbot"
        link = message.text.split()[1]
        
        # Unblock the bot user
        await client.unblock_user(bot_username)
        
        processing_message = await message.reply("<code>processing . . .</code>")
        bot_message = await client.send_message(bot_username, link)
        
        # Wait for the bot to process the link
        await asyncio.sleep(10)
        
        try:
            # Get the response message from the bot
            media_message = await client.get_messages(bot_username, bot_message.id + 2)
            await media_message.copy(message.chat.id, reply_to_message_id=message.id)
            await processing_message.delete()
        except Exception:
            await processing_message.edit(
                "<b>video tidak ditemukan silahkan ulangi beberapA saat lagi</b>"
            )
        
        # Delete the chat history with the bot
        user_info = await client.resolve_peer(bot_username)
        return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))
