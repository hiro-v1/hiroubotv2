
# Copyright (C) 2024 dante
# Credit by dante
# Recode by dante


import asyncio
from pyrogram import *
from DanteUserbot import *

__MODULE__ = "ᴋᴀsᴀʀ⁴"
__HELP__ = f"""
**--Ngatain⁴--**

<blockquote><b>
`lipkol` - coba aja.
`nakal` - coba aja.
`favboy` - coba aja.
`favgirl` - coba aja.
`canlay` - coba aja.
`ganlay` - coba aja.
`cange` - coba aja.</b></blockquote>
"""

@DANTE.UBOT("lipkol")
async def lipkol(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    dante = await message.reply("**Ayaaang** 🥺")
    await asyncio.sleep(1.8)
    await dante.edit("**Kangeeen** 👉👈")
    await asyncio.sleep(1.8)
    await dante.edit("**Pingiinn Slipkool Yaaang** 🥺👉👈")


@DANTE.UBOT("nakal")
async def nakal(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    dante = await message.reply("**Ayaaang Ih** 🥺", reply_to_message_id=ReplyCheck(message))
    await asyncio.sleep(1.8)
    await dante.edit("**Nakal Banget Dah Ayang** 🥺")
    await asyncio.sleep(1.8)
    await dante.edit("**Aku Gak Like Ayang** 😠")
    await asyncio.sleep(1.8)
    await dante.edit("**Pokoknya Aku Gak Like Ih** 😠")


@DANTE.UBOT("favboy")
async def favboy(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    dante = await message.reply(
        "**Duuhh Ada Cowo Ganteng** 👉👈", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.8)
    await dante.edit("**You Are My Favorit Boy** 😍")
    await asyncio.sleep(1.8)
    await dante.edit("**Kamu Harus Jadi Cowo Aku Ya** 😖")
    await asyncio.sleep(1.8)
    await dante.edit("**Pokoknya Harus Jadi Cowo Aku** 👉👈")
    await asyncio.sleep(1.8)
    await dante.edit("**Gak Boleh Ada Yang Lain** 😠")


@DANTE.UBOT("favgirl")
async def favgirl(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    dante = await message.reply(
        "**Duuhh Ada Cewe Cantik** 👉👈", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.8)
    await dante.edit("**You Are My Favorit Girl** 😍")
    await asyncio.sleep(1.8)
    await dante.edit("**Kamu Harus Jadi Cewe Aku Ya** 😖")
    await asyncio.sleep(1.8)
    await dante.edit("**Pokoknya Harus Jadi Cewe Aku** 👉👈")
    await asyncio.sleep(1.8)
    await dante.edit("**Gak Boleh Ada Yang Lain** 😠")


@DANTE.UBOT("canlay")
async def canlay(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    dante = await message.reply(
        "**Eh Kamu Cantik-cantik**", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.8)
    await dante.edit("**Kok Alay Banget**")
    await asyncio.sleep(1.8)
    await dante.edit("**Spam Bot Mulu**")
    await asyncio.sleep(1.8)
    await dante.edit("**Baru Bikin Userbot Ya??**")
    await asyncio.sleep(1.8)
    await dante.edit("**Pantes Norak Xixixi**")


@DANTE.UBOT("ganlay")
async def ganlay(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    dante = await message.reply(
        "**Eh Kamu Ganteng-ganteng**", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.8)
    await dante.edit("**Kok Alay Banget**")
    await asyncio.sleep(1.8)
    await dante.edit("**Spam Bot Mulu**")
    await asyncio.sleep(1.8)
    await dante.edit("**Baru Bikin Userbot Ya??**")
    await asyncio.sleep(1.8)
    await dante.edit("**Pantes Norak Xixixi**")


@DANTE.UBOT("cange")
async def cange(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    dante = await message.reply("**Ayanggg 😖**", reply_to_message_id=ReplyCheck(message))
    await asyncio.sleep(1.8)
    await dante.edit("**Aku Ange 😫**")
    await asyncio.sleep(1.8)
    await dante.edit("**Ayuukk Picies Yang 🤤**")
