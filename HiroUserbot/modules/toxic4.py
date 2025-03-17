
# Copyright (C) 2024 hiro
# Credit by hiro
# Recode by hiro


import asyncio
from pyrogram import *
from HiroUserbot import *

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

@HIRO.UBOT("lipkol")
async def lipkol(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    hiro = await message.reply("**Ayaaang** 🥺")
    await asyncio.sleep(1.8)
    await hiro.edit("**Kangeeen** 👉👈")
    await asyncio.sleep(1.8)
    await hiro.edit("**Pingiinn Slipkool Yaaang** 🥺👉👈")


@HIRO.UBOT("nakal")
async def nakal(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    hiro = await message.reply("**Ayaaang Ih** 🥺", reply_to_message_id=ReplyCheck(message))
    await asyncio.sleep(1.8)
    await hiro.edit("**Nakal Banget Dah Ayang** 🥺")
    await asyncio.sleep(1.8)
    await hiro.edit("**Aku Gak Like Ayang** 😠")
    await asyncio.sleep(1.8)
    await hiro.edit("**Pokoknya Aku Gak Like Ih** 😠")


@HIRO.UBOT("favboy")
async def favboy(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    hiro = await message.reply(
        "**Duuhh Ada Cowo Ganteng** 👉👈", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.8)
    await hiro.edit("**You Are My Favorit Boy** 😍")
    await asyncio.sleep(1.8)
    await hiro.edit("**Kamu Harus Jadi Cowo Aku Ya** 😖")
    await asyncio.sleep(1.8)
    await hiro.edit("**Pokoknya Harus Jadi Cowo Aku** 👉👈")
    await asyncio.sleep(1.8)
    await hiro.edit("**Gak Boleh Ada Yang Lain** 😠")


@HIRO.UBOT("favgirl")
async def favgirl(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    hiro = await message.reply(
        "**Duuhh Ada Cewe Cantik** 👉👈", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.8)
    await hiro.edit("**You Are My Favorit Girl** 😍")
    await asyncio.sleep(1.8)
    await hiro.edit("**Kamu Harus Jadi Cewe Aku Ya** 😖")
    await asyncio.sleep(1.8)
    await hiro.edit("**Pokoknya Harus Jadi Cewe Aku** 👉👈")
    await asyncio.sleep(1.8)
    await hiro.edit("**Gak Boleh Ada Yang Lain** 😠")


@HIRO.UBOT("canlay")
async def canlay(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    hiro = await message.reply(
        "**Eh Kamu Cantik-cantik**", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.8)
    await hiro.edit("**Kok Alay Banget**")
    await asyncio.sleep(1.8)
    await hiro.edit("**Spam Bot Mulu**")
    await asyncio.sleep(1.8)
    await hiro.edit("**Baru Bikin Userbot Ya??**")
    await asyncio.sleep(1.8)
    await hiro.edit("**Pantes Norak Xixixi**")


@HIRO.UBOT("ganlay")
async def ganlay(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    hiro = await message.reply(
        "**Eh Kamu Ganteng-ganteng**", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.8)
    await hiro.edit("**Kok Alay Banget**")
    await asyncio.sleep(1.8)
    await hiro.edit("**Spam Bot Mulu**")
    await asyncio.sleep(1.8)
    await hiro.edit("**Baru Bikin Userbot Ya??**")
    await asyncio.sleep(1.8)
    await hiro.edit("**Pantes Norak Xixixi**")


@HIRO.UBOT("cange")
async def cange(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    hiro = await message.reply("**Ayanggg 😖**", reply_to_message_id=ReplyCheck(message))
    await asyncio.sleep(1.8)
    await hiro.edit("**Aku Ange 😫**")
    await asyncio.sleep(1.8)
    await hiro.edit("**Ayuukk Picies Yang 🤤**")
