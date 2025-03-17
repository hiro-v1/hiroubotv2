from HiroUserbot import *

__MODULE__ = "ᴘʀᴏғɪʟ"
__HELP__ = f"""<blockquote><b>
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴘʀᴏꜰɪʟᴇ 』</b>

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ꜱᴇᴛʙɪᴏ</code> [ᴛᴇxᴛ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ʙɪᴏ ᴀɴᴅᴀ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ꜱᴇᴛɴᴀᴍᴇ</code> [ᴛᴇxᴛ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ɴᴀᴍᴀ ᴀɴᴅᴀ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ʙʟᴏᴄᴋ</code> [ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙʟᴏᴋɪʀ ᴘᴇɴɢɢᴜɴᴀ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ᴜɴʙʟᴏᴄᴋ</code> [ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴋᴀ ʙʟᴏᴋɪʀ ᴘᴇɴɢɢᴜɴᴀ
</b></blockquote>"""

import os
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message

@HIRO.UBOT("setbio")
async def _(client, message):
    tex = await message.reply("ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .")
    if len(message.command) == 1:
        return await tex.edit("berikan tekꜱ untuk ditetapkan ꜱebagai bio.")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await tex.edit(f"<b>berhaꜱil mengubah bio menjadi</b> <code>{bio}</code>")
        except Exception as e:
            await tex.edit(f"<b>ERROR:</b> <code>{e}</code>")
    else:
        return await tex.edit("berikan tekꜱ untuk ditetapkan ꜱebagai bio.")



@HIRO.UBOT("setname")
async def _(client, message):
    tex = await message.reply("ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .")
    if len(message.command) == 1:
        return await tex.edit("berikan tekꜱ untuk ditetapkan ꜱebagai nama anda.")
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await tex.edit(
                f"<b>berhaꜱil mengubah nama menjadi</b> <code>{name}</code>"
            )
        except Exception as e:
            await tex.edit(f"<b>ERROR:</b> <code>{e}</code>")
    else:
        return await tex.edit("berikan tekꜱ untuk ditetapkan ꜱebagai nama anda.")




@HIRO.UBOT("block")
async def _(client, message):
    user_id = await extract_user(message)
    tex = await message.reply("ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .")
    if not user_id:
        return await tex.edit(f"berikan nama pengguna untuk diblokir.")
    if user_id == client.me.id:
        return await tex.edit("ok done.")
    await client.block_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f"<b>berhaꜱil diblokir</b> {umention}")


@HIRO.UBOT("unblock")
async def _(client, message):
    user_id = await extract_user(message)
    tex = await message.reply("ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . .")
    if not user_id:
        return await tex.edit("berikan nama pengguna atau balaꜱ peꜱan untuk membuka blokir.")
    if user_id == client.me.id:
        return await tex.edit("ok done.")
    await client.unblock_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f"<b>berhaꜱil dibebaꜱkan</b> {umention}")
