import asyncio
import os

from pyrogram import *
from pyrogram.types import *
from pyrogram import filters, Client
from pyrogram.raw.functions.messages import DeleteHistory
from DanteUserbot.core.helpers.tools import edit_or_reply
from DanteUserbot import *

__MODULE__ = "ᴄᴜʀɪ"
__HELP__ = f"""<blockquote><b>
<b>『 Curi 』</b>

  <b>• perintah:</b> <code>{PREFIX[0]}curi</code>
  <b>• penjelasan:</b> .curi untuk mengambil pap timer
</b></blockquote>
"""

@DANTE.UBOT("curi")
async def pencuri(client, message):
    dia = message.reply_to_message
    me = client.me.id
    if not dia:
        return await edit_or_reply(message, "`Mohon balas ke media.`")
    
    anjing = dia.caption or None
    await edit_or_reply(message, "`Processing...`")
    
    try:
        if dia.text:
            await dia.copy("me")
        elif dia.photo:
            anu = await client.download_media(dia)
            await client.send_photo("me", anu, anjing)
            os.remove(anu)
        elif dia.video:
            anu = await client.download_media(dia)
            await client.send_video("me", anu, anjing)
            os.remove(anu)
        elif dia.audio:
            anu = await client.download_media(dia)
            await client.send_audio("me", anu, anjing)
            os.remove(anu)
        elif dia.voice:
            anu = await client.download_media(dia)
            await client.send_voice("me", anu, anjing)
            os.remove(anu)
        elif dia.document:
            anu = await client.download_media(dia)
            await client.send_document("me", anu, anjing)
            os.remove(anu)
        else:
            return await message.edit(f"{ggl}**sᴇᴘᴇʀᴛɪɴʏᴀ ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ**")
        
        await client.send_message("me", "**Pap timernya tuh.**")
        await message.delete()
    except Exception as e:
        await message.reply_text(str(e))
