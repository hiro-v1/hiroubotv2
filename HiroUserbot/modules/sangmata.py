from HiroUserbot import *
import asyncio
import random
from pyrogram.raw.functions.messages import DeleteHistory

__MODULE__ = "sɢ"
__HELP__ = """
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ꜱᴀɴɢᴍᴀᴛᴀ--**

<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}sg</code> [ᴜꜱᴇʀ_ɪᴅ/ʀᴇᴘʟʏ ᴜꜱᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍᴇʀɪᴋꜱᴀ ʜɪꜱᴛᴏʀɪ ɴᴀᴍᴀ/ᴜꜱᴇʀɴᴀᴍᴇ
</b></blockquote>"""

@HIRO.UBOT("sg")
async def _(client, message):
    get_user = await extract_user(message)
    lol = await message.reply("</b>memproses. . .</b>")
    if not get_user:
        return await lol.edit("<b>user tidak ditemukan</b>")
    try:
        user_id = (await client.get_users(get_user)).id
    except Exception:
        try:
            user_id = int(message.command[1])
        except Exception as error:
            return await lol.edit(error)
    bot = ["@Sangmata_bot", "@SangMata_beta_bot"]
    getbot = random.choice(bot)
    await client.unblock_user(getbot)
    txt = await client.send_message(getbot, user_id)
    await asyncio.sleep(4)
    await txt.delete()
    await lol.delete()
    async for name in client.search_messages(getbot, limit=2):
        if not name.text:
            await message.reply(
                f"❌ {getbot} tidak dapat merespon permintaan", quote=True
            )
        else:
            await message.reply(name.text, quote=True)
    user_info = await client.resolve_peer(getbot)
    return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))
