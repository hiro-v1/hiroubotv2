# Copyright (C) 2024 HIRO
# Credit by HIRO
# Recode by HIRO


import asyncio
from pyrogram import *
from HiroUserbot import *

__MODULE__ = "ᴋᴀsᴀʀ⁵"
__HELP__ = f"""
**--Ngatain⁵--**
<blockquote><b>

`ceking` - coba aja.
`hinaa` - coba aja.
`kaca` - coba aja.</b></blockquote>
"""

@HIRO.UBOT("ceking")
async def ceking(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    sepong = await message.reply(
        "**GIGI KUNING MATA MERAH BADAN KURUS CEKING EMANG PANTES...**",
        reply_to_message_id=ReplyCheck(message),
    )

    await asyncio.sleep(1.8)
    await sepong.edit("**DI KENCINGIN JAHANAM**")
    await asyncio.sleep(1.8)
    await sepong.edit("**ORANG KAYA LUH ITU...**")
    await asyncio.sleep(1.8)
    await sepong.edit("**CUMAN SEMPIT SEMPITIN ISI DUNIA DOANG bapakluTOL SEMPAK**")
    await asyncio.sleep(1.8)
    await sepong.edit("**GUA KASIH TAU NIH YAH USUS LUH TUH UDAH MELINTIR bapakluTOL**")
    await asyncio.sleep(1.8)
    await sepong.edit("**KERONGbapakluGAN LUH ITU UDAH RUSAK TOLOL...**")
    await asyncio.sleep(1.8)
    await sepong.edit(
        "**MASIH AJA MAKSAIN BUAT ADU ROASTING AMA GUA BEGO BANGET SIH LUH...**"
    )


@HIRO.UBOT("hinaa")
async def hinaa(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    bapaklu = await message.reply("**IZIN PANTUN BANG...**", reply_to_message_id=ReplyCheck(message))
    await asyncio.sleep(1.8)
    await bapaklu.edit("**KETEMU SI MAMAS DIAJAKIN KE CIBINONG...**")
    await asyncio.sleep(1.8)
    await bapaklu.edit("**PULANG NYE DIANTERIN MAKE KOPAJA...**")
    await asyncio.sleep(1.8)
    await bapaklu.edit("**EH BOCAH AMPAS TITISAN DAJJAL...**")
    await asyncio.sleep(1.8)
    await bapaklu.edit("**MUKA HINA KEK ODONG ODONG**")
    await asyncio.sleep(1.8)
    await bapaklu.edit("**GA USAH SO KERAS DEH LU KALO MENTAL BLOM SEKERAS BAJA...**")
    await asyncio.sleep(1.8)
    await bapaklu.edit("**LUH ITU MANUSIA...**")
    await asyncio.sleep(1.8)
    await bapaklu.edit("**MANUSIA HINA YANG DI CIPTAKAN DENGAN SECARA HINA**")
    await asyncio.sleep(1.8)
    await bapaklu.edit(
        "**MANUSIA HINA YANG DI CIPTAKAN DENGAN SECARA HINA EMANG PANTES UNTUK DI HINA HINA...**"
    )


@HIRO.UBOT("kaca")
async def kaca(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.id in DEVS:
        await message.reply("**AKUN LO MO ILANG BANGSAT??**")
        return
    omek = await message.reply(
        "**IZIN NUMPANG PANTUN BANG...**", reply_to_message_id=ReplyCheck(message)
    )
    await asyncio.sleep(1.8)
    await omek.edit("**BELI SEPATU KACA KE CHINA...**")
    await asyncio.sleep(1.8)
    await omek.edit("**ASEEEKKKK 🤪**")
    await asyncio.sleep(1.8)
    await omek.edit("**NGACA DULU BARU NGEHINA bapakluTOL...**")
    await asyncio.sleep(1.8)
    await omek.edit("**UDAH BULUK ITEM PENDEK BERPONI BAJU KEGEDEAN KAYAK JAMET**")
    await asyncio.sleep(1.8)
    await omek.edit(
        "**UDAH BULUK ITEM PENDEK BERPONI BAJU KEGEDEAN KAYAK JAMET SOK-SOK AN MAU NGEHINA GUA bapakluTOL**"
    )
    await asyncio.sleep(1.8)
    await omek.edit("**KENA KAN MENTAL LU...**")
