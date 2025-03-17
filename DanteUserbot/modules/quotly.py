from DanteUserbot import *

__MODULE__ = "ǫᴜᴏᴛʟʏ"
__HELP__ = f"""<blockquote><b>
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ զᴜᴏᴛʟʏ 』</b>

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}զ</code> [ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇʀᴜʙᴀʜ ᴛᴇxᴛ ᴍᴇɴᴊᴀᴅɪ ꜱᴛɪᴄᴋᴇʀ
</b></blockquote>"""

import asyncio
import os
from pyrogram.raw.functions.messages import DeleteHistory

@DANTE.UBOT("q")
async def _(client, message):
    info = await eor(message, "<b>memproses.....</b>")
    await client.unblock_user("@QuotLyBot")
    if message.reply_to_message:
        if len(message.command) < 2:
            msg = [message.reply_to_message]
        else:
            try:
                count = int(message.command[1])
            except Exception as error:
                await info.edit(error)
            msg = [
                i
                for i in await client.get_messages(
                    chat_id=message.chat.id,
                    message_ids=range(
                        message.reply_to_message.id, message.reply_to_message.id + count
                    ),
                    replies=-1,
                )
            ]
        try:
            for x in msg:
                await x.forward("@QuotLyBot")
        except Exception:
            pass
        await asyncio.sleep(9)
        await info.delete()
        async for quotly in client.get_chat_history("@QuotLyBot", limit=1):
            if not quotly.sticker:
                await eor(
                    "message, ❌ @QuotLyBot tidak dapat merespon permintAan"
                )
            else:
                sticker = await client.download_media(quotly)
                await message.reply_sticker(sticker, quote=True)
                os.remove(sticker)
    else:
        if len(message.command) < 2:
            return await info.edit("<b>reply to text/media</b>")
        else:
            msg = await client.send_message(
                "@QuotLyBot", f"/qcolor {message.command[1]}"
            )
            await asyncio.sleep(1)
            get = await client.get_messages("@QuotLyBot", msg.id + 1)
            await info.edit(
                f"<b>warna latar belakang kutipan disetel ke:</b> <code>{get.text.split(':')[1]}</code>"
            )
    user_info = await client.resolve_peer("@QuotLyBot")
    return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))

