from datetime import datetime
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from DanteUserbot import *

@DANTE.UBOT("stats")
async def stats(client: Client, message: Message) -> None:
    Man = await message.edit_text("`Mengambil info akun ...`")
    start = datetime.now()
    u, g, sg, c, b, a_chat = 0, 0, 0, 0, 0, 0
    Meh = await client.get_me()
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == enums.ChatType.BOT:
            b += 1
        elif dialog.chat.type == enums.ChatType.GROUP:
            g += 1
        elif dialog.chat.type == enums.ChatType.SUPERGROUP:
            sg += 1
            user_s = await dialog.chat.get_member(int(Meh.id))
            if user_s.status in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ):
                a_chat += 1
        elif dialog.chat.type == enums.ChatType.CHANNEL:
            c += 1

    end = datetime.now()
    ms = (end - start).seconds
    await Man.edit_text(
        f"""`📊 Status akun anda, berhasil diambil dalam {ms} detik`
`💬 {u} Pesan Pribadi.`
`👥 berada di {g} Groups.`
`👥 berada {sg} Super Groups.`
`📢 berada {c} Channels.`
`🔧 menjadi admin di {a_chat} Chats.`
`🤖 Bots = {b}`"""
    )

__MODULE__ = "sᴛᴀᴛs"
__HELP__ = """
 **--Bantuan Untuk Stats--**

<blockquote><b>
๏ Perintah: <code>stats</code>
◉ Penjelasan: Melihat informasi akun anda.</b></blockquote>
"""
