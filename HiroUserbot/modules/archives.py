from HiroUserbot import *
from pyrogram.enums import ChatType
from asyncio import sleep

__MODULE__ = "ᴀʀᴄʜɪᴠᴇ"
__HELP__ = """
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴀʀᴄʜɪᴠᴇ--**
<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}archiveall</code> ɢᴄ ᴘᴠ
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀʀᴄʜɪᴠᴇᴋᴀɴ ꜱᴇᴍᴜᴀ ᴘᴇꜱᴀɴ ᴘʀɪʙᴀᴅɪ
  <b>• ᴄᴏɴᴛᴏʜ : </b> <code>{0}ᴀʀᴄʜɪᴠᴇᴀʟʟ</code> ɢᴄ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}unarchiveall</code> ɢᴄ ᴘᴠ
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀʀᴄʜɪᴠᴇᴋᴀɴ ꜱᴇᴍᴜᴀ ᴘᴇꜱᴀɴ ᴘʀɪʙᴀᴅɪ
  <b>• ᴄᴏɴᴛᴏʜ : </b> <code>{0}ᴜɴᴀʀᴄʜɪᴠᴇᴀʟʟ</code> ɢᴄ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}archive</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀʀᴄʜɪᴠᴇᴋᴀɴ ᴘᴇꜱᴀɴ ᴄʜᴀᴛ ꜱᴀᴀᴛ ɪɴɪ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}unarchive</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜɴᴀʀᴄʜɪᴠᴇᴋᴀɴ ᴄʜᴀᴛ ꜱᴀᴀᴛ ɪɴɪ
</b></blockquote>
"""


@HIRO.UBOT("archiveall")
async def _(client, message):
    done = 0
    gagal = 0
    ex = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    bsl = await EMO.BERHASIL(client)
    rizal = await message.reply_text(f"<b>{prs}ᴘʀᴏᴄᴄᴇsɪɴɢ...</b>")
    if len(message.command) != 2:
        await rizal.edit(f"{ex}<b>ɢᴜɴᴀᴋᴀɴ ᴛʏᴘᴇ ᴜsᴇʀs ᴀᴛᴀᴜ ɢʀᴏᴜᴘ</b>")
        return

    query = message.command[1]

    chat_ids = await get_data_id(client, query)

    for chat_id in chat_ids:
        await sleep(1)
        try:
            await client.archive_chats(chat_id)
            done += 1
        except:
            gagal += 1
            pass

    await rizal.edit(f"""
<b>{prs}ʙᴇʀʜᴀsɪʟ ᴍᴇɴᴊᴀʟᴀɴᴋᴀɴ ᴀʀᴄʜɪᴠᴇ
{bsl}ʙᴇʀʜᴀsɪʟ : {done} ɢʀᴜᴘ
{ex}ɢᴀɢᴀʟ : {gagal} ɢʀᴜᴘ
""")


@HIRO.UBOT("unarchiveall")
async def _(client, message):
    done = 0
    gagal = 0
    ex = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    bsl = await EMO.BERHASIL(client)
    rizal = await message.reply_text(f"<b>{prs}ᴘʀᴏᴄᴄᴇsɪɴɢ...</b>")
    if len(message.command) != 2:
        await rizal.edit(f"{ex}<b>ɢᴜɴᴀᴋᴀɴ ᴛʏᴘᴇ ᴜsᴇʀs ᴀᴛᴀᴜ ɢʀᴏᴜᴘ</b>")
        return

    query = message.command[1]

    chat_ids = await get_data_id(client, query)

    for chat_id in chat_ids:
        await sleep(1)
        try:
            await client.unarchive_chats(chat_id)
            done += 1
        except:
            gagal += 1
            pass

    await rizal.edit(f"""
<b>{prs}ʙᴇʀʜᴀsɪʟ ᴍᴇɴᴊᴀʟᴀɴᴋᴀɴ ᴜɴᴀʀᴄʜɪᴠᴇ
{bsl}ʙᴇʀʜᴀsɪʟ : {done} ɢʀᴜᴘ
{ex}ɢᴀɢᴀʟ : {gagal} ɢʀᴜᴘ</b>
""")


@HIRO.UBOT("archive")
async def _(client, message):
    bsl = await EMO.BERHASIL(client)
    ex = await EMO.GAGAL(client)
    user_id = message.chat.id
    c = await client.archive_chats(user_id)
    if c:
        await message.reply_text(f"{bsl}<b>ʙᴇʀʜᴀsɪʟ ᴍᴇɴɢ ᴀʀᴄʜɪᴠᴇᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ</b>")
    else:
        await message.reply_text(f"{ex}<b>ɢᴀɢᴀʟ ᴍᴇɴɢ ᴀʀᴄʜɪᴠᴇᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ</b>")

@HIRO.UBOT("unarchive")
async def _(client, message):
    bsl = await EMO.BERHASIL(client)
    ex = await EMO.GAGAL(client)
    user_id = message.chat.id
    c = await client.archive_chats(user_id)
    if c:
        await message.reply_text(f"{bsl}<b>ʙᴇʀʜᴀsɪʟ ᴍᴇɴɢᴜɴ ᴀʀᴄʜɪᴠᴇᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ..</b>")
    else:
        await message.reply_text(f"{ex}<b>ɢᴀɢᴀʟ ᴍᴇɴɢᴜɴ ᴀʀᴄʜɪᴠᴇᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ</b>")
