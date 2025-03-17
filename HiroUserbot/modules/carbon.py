from HiroUserbot import *

__MODULE__ = "ᴄᴀʀʙᴏɴ"
__HELP__ = f"""
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ꜰᴏɴᴛ--**
<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}carbon</code> [ʀᴇᴘʟʏ/ᴛᴇxᴛ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴛᴇᴋꜱ ᴄᴀʀʙᴏɴᴀʀᴀ</b></blockquote>
"""
from io import BytesIO
from HiroUserbot.core.function.emoji import emoji

async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


async def carbon_func(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    ex = await message.reply(f"{prs}**ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .**")
    carbon = await make_carbon(text)
    await ex.edit(f"{prs}**ᴜᴘʟᴏᴀᴅɪɴɢ . . .**")
    await asyncio.gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"{sks}<b>ᴄᴀʀʙᴏɴɪꜱᴇᴅ ʙʏ :</b>{client.me.mention}",
        ),
    )
    carbon.close()

@HIRO.UBOT("carbon")
async def _(client, message):
    await carbon_func(client, message)
