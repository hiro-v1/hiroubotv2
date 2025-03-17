import asyncio
from pyrogram import *
from HiroUserbot import *

__MODULE__ = "ᴋᴀsᴀʀ³"
__HELP__ = f"""
**--Ngatain³--**

<blockquote><b>
`ganteng` - coba aja.
`wibu` - coba aja.
`senggol` - coba aja.</b></blockquote>
"""

@HIRO.UBOT("ganteng")
async def ganteng(client, message):
    HIRO = await message.reply(
        "`Lu Mau Tau Sebuah Fakta?`", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.2)
    await HIRO.edit("`Fakta Yang Belum Terbongkar Selama Ini`")
    await asyncio.sleep(1.2)
    await HIRO.edit("**GUA GANTENG FIX NO DEBAT😏**")


@HIRO.UBOT("wibu")
async def wibu(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    HIRO = await message.reply("`Kata Emak`", reply_to_message_id=ReplyCheck(message))
    await asyncio.sleep(2)
    await HIRO.edit("`Kalo Ketemu Wibuu`")
    await asyncio.sleep(2)
    await HIRO.edit("`Harus Lari Sekenceng Mungkin🏃🏻`")
    await asyncio.sleep(3)
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`ㅤ🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`🏃🏻💨ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ`")
    await HIRO.edit("`🧎🏻‍♂️ huhh... akhirnya bisa lolos dari wibu mematikan`")


@HIRO.UBOT("senggol")
async def senggol(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    HIRO = await message.reply(
        "`Bapaknya Udin Di Makan Singkong`", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.8)
    await HIRO.edit("`Cuma Sendiri ni Senggol Dong`")
