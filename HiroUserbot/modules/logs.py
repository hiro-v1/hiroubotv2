from HiroUserbot import *

__MODULE__ = "ʟᴏɢs"
__HELP__ = f"""<blockquote><b>
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʟᴏɢs 』</b>

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}logs</code> [ᴛʏᴘᴇ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ʟᴏɢs

  <b>• ᴛʏᴘᴇ : on/off</b></blockquote>
"""

@HIRO.UBOT("logs")
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    if len(message.command) < 2:
        return await message.reply(
            f"{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b>"
        )

    query = {"on": True, "off": False, "none": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(f"<b>{ggl}opsi tidak valid!!</b>")

    value = query[command]

    await set_vars(client.me.id, "ON_LOGS", value)
    return await message.reply(
        f"<b>{brhsl}LOGS berhasil disetting ke:</b> {value}"
    )


@HIRO.NO_CMD_UBOT("LOGS_GROUP", ubot)
async def _(client, message):
    on_logs = await get_vars(client.me.id, "ON_LOGS")
    if on_logs:
        user_link = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
        message_link = message.link
        message_text = f"""
<b>🤖 ᴀᴅᴀ ᴘᴇsᴀɴ ᴍᴀsᴜᴋ ᴅᴀʀɪ {message.chat.title} </b>
<b>👤 ᴘᴇɴɢɢᴜɴᴀ : {message.from_user.first_name} </b>
<b>🗯 ᴘᴇsᴀɴ : </b><code>{message.text}</b>
"""
        await bot.send_message(
            client.me.id,
            message_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ɢʀᴜᴘ", url=f"{message_link}")],
            ]))
