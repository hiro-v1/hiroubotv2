import asyncio
import random

from gc import get_objects
from asyncio import sleep

from pyrogram.errors.exceptions import FloodWait

from DanteUserbot import *

__MODULE__ = 'ᴡᴏʀᴅ ᴘʀᴏᴛᴇᴄᴛ'
__HELP__ = f"""<blockquote><b>
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴘᴇɴɢᴇɴᴅᴀʟɪᴀɴ ᴋᴀᴛᴀ 』</b>

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}addword</code> [ᴋᴀᴛᴀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴋᴀᴛᴀ ᴋᴇ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ ᴘʀᴏᴛᴇᴋsɪ.

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}listword</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴍᴇɴᴀᴍᴘɪʟᴋᴀɴ ᴅᴀғᴛᴀʀ ᴋᴀᴛᴀ ʏᴀɴɢ ᴛᴇʟᴀʜ ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ.

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}delword</code> [ᴋᴀᴛᴀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴍᴇɴɢʜᴀᴘᴜs ᴋᴀᴛᴀ ᴅᴀʀɪ ᴅᴀғᴛᴀʀ ᴘʀᴏᴛᴇᴋsɪ.

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}bl</code> [ᴏɴ/ᴏғғ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴍᴇɴʏᴀʟᴀᴋᴀɴ ᴀᴛᴀᴜ ᴍᴇᴍᴀᴛɪᴋᴀɴ ᴘᴇɴɢᴇɴᴅᴀʟɪᴀɴ ᴋᴀᴛᴀ.
</b></blockquote>"""


@DANTE.UBOT("addword")
@DANTE.GROUP
async def _(client, message):
    vars = await get_vars(client.me.id, "WORD_LIST") or []
    text = get_arg(message).split()
   
    add_word = [x for x in text if x not in vars]
    vars.extend(add_word)
    await set_vars(client.me.id, "WORD_LIST", vars)
   
    if add_word:
        response = (
            f"<b>ʙᴇʀʜᴀsɪʟ ᴅɪᴛᴀᴍʙᴀʜ ᴋᴇ ᴘʀᴏᴛᴇᴄᴛ</b>\n"
            f"<b>ᴋᴀᴛᴀ ʏᴀɴɢ ᴅɪᴛᴀᴍʙᴀʜ:</b> {''.join(add_word)}"
        )
    else:
        response = "<b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴋᴀᴛᴀ ʏᴀɴɢ ᴅɪᴛᴀᴍʙᴀʜ.</b>"

    return await message.reply(response)


@DANTE.UBOT("listword")
@DANTE.GROUP
async def _(client, message):
    vars = await get_vars(client.me.id, "WORD_LIST") or []
    if vars:
        msg = "<b>❏ ᴅᴀғᴛᴀʀ ᴡᴏʀᴅ</b>\n\n"
        for x in vars:
            msg += f" • {x}\n"
        msg += f"<b>\n❏ ᴛᴏᴛᴀʟ ᴡᴏʀᴅ: {len(vars)}</b>"
    else:
        msg = "<b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴡᴏʀᴅ</b>"
        
    return await message.reply(msg, quote=True)


@DANTE.UBOT("delword")
@DANTE.GROUP
async def _(client, message):
    vars = await get_vars(client.me.id, "WORD_LIST") or []
    _, *text = message.command
    cleaned_text = [word for word in text if word.isalnum()]
    removed_list = [x for x in cleaned_text if x in vars]
    vars = [x for x in vars if x not in removed_list]
    await set_vars(client.me.id, "WORD_LIST", vars)

    if removed_list:
        response = (
            f"<b>ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ᴘʀᴏᴛᴇᴄᴛ</b>\n"
            f"<b>ᴋᴀᴛᴀ ʏᴀɴɢ ᴅɪʜᴀᴘᴜs:</b> {''.join(removed_list)}"
        )
    else:
        response = "<b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴋᴀᴛᴀ ʏᴀɴɢ ᴅɪʜᴀᴘᴜs.</b>"

    return await message.reply(response)


@DANTE.UBOT("bl")
async def set_kata(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    if len(message.command) < 2:
        return await message.reply(
            f"{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b>"
        )    
    action = message.command[1].lower()
    if action == "on":
        await set_status(client.me.id, True)
        await message.reply(f"{brhsl}<b>word detection is now on.</b>")
    elif action == "off":
        await set_status(client.me.id, False)
        await message.reply(f"{ggl}<b>word detection is now off.</b>")
    else:
        return await message.reply(
            f"{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b>"
        )
