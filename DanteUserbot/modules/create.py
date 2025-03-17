from DanteUserbot import *

__MODULE__ = "ᴄʀᴇᴀᴛᴇ"
__HELP__ = """<blockquote><b>
 <b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄʀᴇᴀᴛᴇ 』</b>

<b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}buat</code> ɢᴄ ɴᴀᴍᴀɢᴄ
<b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ɢʀᴜᴘ ᴛᴇʟᴇɢʀᴀᴍ.

<b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}buat</code> ᴄʜ ɴᴀᴍᴀᴄʜ
<b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴄʜᴀɴɴᴇʟ ᴛᴇʟᴇɢʀᴀᴍ.</b></blockquote>
"""

import os
from DanteUserbot.core.function.emoji import emoji


@DANTE.UBOT("buat")
async def create_grup(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    if len(message.command) < 3:
        return await message.reply(
            f"{ggl}**sɪʟᴀʜᴋᴀɴ ᴋᴇᴛɪᴋ** `{message.command}` **ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ʙᴀɴᴛᴜᴀɴ ᴅᴀʀɪ ᴍᴏᴅᴜʟ ɪɴɪ**"
        )
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    xd = await message.reply(f"{prs}<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs</b>...")
    desc = "Welcome To My " + ("Group" if group_type == "gc" else "Channel")
    try:
        if group_type == "gc":
            _id = await client.create_supergroup(group_name, desc)
            link = await client.get_chat(_id.id)
            await xd.edit(
                f"{sks}<b>ʙᴇʀʜᴀsɪʟ ᴍᴇᴍʙᴜᴀᴛ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴜᴘ</b> : [{group_name}]({link.invite_link})",
                disable_web_page_preview=True,
            )
        elif group_type == "ch":
            _id = await client.create_channel(group_name, desc)
            link = await client.get_chat(_id.id)
            await xd.edit(
                f"{sks}<b>ʙᴇʀʜᴀsɪʟ ᴍᴇᴍʙᴜᴀᴛ ᴛᴇʟᴇɢʀᴀᴍ ᴄʜᴀɴɴᴇʟ : [{group_name}]({link.invite_link})</b>",
                disable_web_page_preview=True,
            )
    except Exception as r:
        await xd.edit(f"{ggl}ᴇʀʀᴏʀ : {r}")
