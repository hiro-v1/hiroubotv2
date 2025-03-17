from DanteUserbot import *
import asyncio
from pyrogram.enums import ChatType, MessageEntityType


__MODULE__ = "ʙᴀʟᴀs"
__HELP__ = """
**--balas semua chat digroup--**
<blockquote><b>
.rep replay text
note: balas ke pesan kamu sendiri contoh : hai replay kepesan kamu, maka semua pesan yang kamu replay tadi akan membalas ke semua group
</b></blockquote>"""

@DANTE.UBOT("rep")
async def asu(client, message):
    if len(message.command) < 2:  # Periksa apakah ada argumen setelah kata kunci 'asu'
        return await message.reply("gunakan rep balasan")
    x = await message.reply(f"proccesing...")
    done = 0
    gagal = 0
    anjir = " ".join(message.command[1:])  # Menggabungkan semua elemen setelah elemen pertama

    # Check if the user is a Telegram Premium subscriber
    user = await client.get_users(message.from_user.id)
    is_premium = user.is_premium

    async for ngentod in client.get_dialogs():
        if ngentod.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            pesan = client.get_chat_history(
                chat_id=ngentod.chat.id,
                limit=15)
            async for message in pesan:
                if message.mentioned:
                    try:
                        if is_premium:
                            hai = await message.reply(f"{anjir}", entities=[{"type": MessageEntityType.CUSTOM_EMOJI, "offset": 0, "length": len(anjir)}])
                        else:
                            hai = await message.reply(f"{anjir}")
                        if hai:
                            done += 1
                    except:
                        gagal += 1
                        pass
    await x.edit(f"berhasil reply ke : {done} chat\ngagal reply ke : {gagal} chat")
