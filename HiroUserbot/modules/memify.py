from HiroUserbot import *

__MODULE__ = "ᴍᴇᴍᴇғʏ"
__HELP__ = f"""<blockquote><b>
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴍᴇᴍɪꜰʏ 』</b>

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}mmf</code> [ᴛᴇxᴛ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ʙᴀʟᴀꜱ ᴋᴇ ꜱᴛɪᴄᴋᴇʀ ᴀᴛᴀᴜ ꜰᴏᴛᴏ ᴀᴋᴀɴ ᴅɪ ᴜʙᴀʜ ᴍᴇɴᴊᴀᴅɪ ꜱᴛɪᴄᴋᴇʀ ᴛᴇᴋꜱ ᴍᴇᴍᴇ ʏᴀɴɢ ᴅɪ ᴛᴇɴᴛᴜᴋᴀɴ
</b></blockquote>"""

import asyncio
import os
from HiroUserbot.core.function.emoji import emoji

@HIRO.UBOT("mmf|memify")
async def memify_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply( "balas ke pesan foto atau sticker!")
    reply_message = message.reply_to_message
    if not reply_message.media:
        return await message.reply( "balas ke pesan foto atau sticker")
    file = await client.download_media(reply_message)
    Tm = await message.reply( "processing . . .")
    text = get_arg(message)
    if len(text) < 1:
        return await Tm.edit( f"harap ketik {PREFIX[0]}mmf text")
    meme = await add_text_img(file, text)
    await asyncio.gather(
        Tm.delete(),
        client.send_sticker(
            message.chat.id,
            sticker=meme,
            reply_to_message_id=message.id,
        ),
    )
    os.remove(meme)
