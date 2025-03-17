import asyncio
from pyrogram import *
from DanteUserbot import *

__MODULE__ = "ᴋᴀsᴀʀ³"
__HELP__ = f"""
**--Ngatain³--**

<blockquote><b>
`ganteng` - coba aja.
`wibu` - coba aja.
`senggol` - coba aja.</b></blockquote>
"""

@DANTE.UBOT("ganteng")
async def ganteng(client, message):
    dante = await message.reply(
        "`Lu Mau Tau Sebuah Fakta?`", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.2)
    await dante.edit("`Fakta Yang Belum Terbongkar Selama Ini`")
    await asyncio.sleep(1.2)
    await dante.edit("**GUA GANTENG FIX NO DEBAT😏**")


@DANTE.UBOT("wibu")
async def wibu(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    dante = await message.reply("`Kata Emak`", reply_to_message_id=ReplyCheck(message))
    await asyncio.sleep(2)
    await dante.edit("`Kalo Ketemu Wibuu`")
    await asyncio.sleep(2)
    await dante.edit("`Harus Lari Sekenceng Mungkin🏃🏻`")
    await asyncio.sleep(3)
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`ㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await dante.edit("`🧎🏻‍♂️ huhh... akhirnya bisa lolos dari wibu mematikan`")


@DANTE.UBOT("senggol")
async def senggol(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    dante = await message.reply(
        "`Bapaknya Udin Di Makan Singkong`", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.8)
    await dante.edit("`Cuma Sendiri ni Senggol Dong`")
