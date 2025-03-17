from DanteUserbot import *

__MODULE__ = "ᴘᴜʀɢᴇ"
__HELP__ = f"""<blockquote><b>
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴘᴜʀɢᴇ 』</b>

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ᴘᴜʀɢᴇ</code> [ʀᴇᴘʟʏ ᴛᴏ ᴍᴇꜱꜱᴀɢᴇ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ʙᴇʀꜱɪʜᴋᴀɴ (ʜᴀᴘᴜꜱ ꜱᴇᴍᴜᴀ ᴘᴇꜱᴀɴ) ᴏʙʀᴏʟᴀɴ ᴅᴀʀɪ ᴘᴇꜱᴀɴ ʏᴀɴɢ ᴅɪʙᴀʟᴀꜱ ʜɪɴɢɢᴀ ʏᴀɴɢ ᴛᴇʀᴀᴋʜɪʀ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ᴅᴇʟ</code> [ʀᴇᴘʟʏ ᴛᴏ ᴍᴇꜱꜱᴀɢᴇ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ʜᴀᴘᴜꜱ ᴘᴇꜱᴀɴ ʏᴀɴɢ ᴅɪʙᴀʟᴀꜱ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ᴘᴜʀɢᴇᴍᴇ</code> [ɴᴜᴍʙᴇʀ ᴏꜰ ᴍᴇꜱꜱᴀɢᴇꜱ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ʜᴀᴘᴜꜱ ᴘᴇꜱᴀɴ ᴀɴᴅᴀ ꜱᴇɴᴅɪʀɪ ᴅᴇɴɢᴀɴ ᴍᴇɴᴇɴᴛᴜᴋᴀɴ ᴛᴏᴛᴀʟ ᴘᴇꜱᴀɴ
</b></blockquote>"""

import asyncio
from DanteUserbot.core.function.emoji import emoji


@DANTE.UBOT("del")
async def del_cmd(client, message):
    rep = message.reply_to_message
    await message.delete()
    try:
        await rep.delete()
    except AttributeError:
        pass



@DANTE.UBOT("purgeme")
async def purgeme_cmd(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    if len(message.command) != 2:
        return await message.delete()
    n = (
        message.reply_to_message
        if message.reply_to_message
        else message.text.split(None, 1)[1].strip()
    )
    if not n.isnumeric():
        return await message.reply(f"{ggl}<b>ᴀʀɢᴜᴍᴇɴ ᴛɪᴅᴀᴋ ᴠᴀʟɪᴅ</b>")
    n = int(n)
    if n < 1:
        return await message.reply(f"{ggl}<b>ʙᴜᴛᴜʜ ɴᴏᴍᴇʀ >=1-999</b>")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user=int(message.from_user.id),
            limit=n,
        )
    ]
    if not message_ids:
        return await message.reply_text(f"{ggl}<b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇsᴀɴ ʏᴀɴɢ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
    to_delete = [message_ids[i : i + 999] for i in range(0, len(message_ids), 999)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
        mmk = await message.reply(f" {n} <b>ᴘᴇsᴀɴ ᴛᴇʟᴀʜ ᴅɪ ʜᴀᴘᴜs</b>")
        await asyncio.sleep(2)
        await mmk.delete()

@DANTE.UBOT("purge")
async def purge_cmd(client, message):
    ggl = await EMO.GAGAL(client)
    await message.delete()
    if not message.reply_to_message:
        return await message.reply_text(f"<b>{ggl}ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ ᴜɴᴛᴜᴋ ᴅɪʙᴇʀsɪʜᴋᴀɴ</b>.")
    chat_id = message.chat.id
    message_ids = []
    for message_id in range(
        message.reply_to_message.id,
        message.id,
    ):
        message_ids.append(message_id)
        if len(message_ids) == 100:
            await client.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            message_ids = []
    if len(message_ids) > 0:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )

