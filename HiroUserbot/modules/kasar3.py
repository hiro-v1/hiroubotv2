from HiroUserbot import *

import asyncio

from pyrogram import filters
from pyrogram.types import Message

from HiroUserbot.core.helpers.tools import edit_or_reply, extract_user, ReplyCheck

__MODULE__ = "ᴋᴀsᴀʀ³"
__HELP__ = f"""<blockquote><b>
❏<b>『 Ngatain²』</b>
├• `palsu` - coba aja.
├• `nyanyi` - coba aja.
├• `p` - coba aja.
╰• `yameteh` - coba aja.</b></blockquote>
"""



@HIRO.UBOT("palsu")
async def toxicpalsu(ubot: ubot, message: Message):
    user_id = await extract_user(message)
    if user_id in DEVS:
        return await edit_or_reply(
            message, "**Perintah ini Dilarang digunakan Kepada Developer Saya**"
        )
    xx = await edit_or_reply(message, "OII ANAK ANYINGG")
    await asyncio.sleep(1.5)
    await xx.edit("KOK PP NYA BEDA SAMA WAJAH NYA")
    await asyncio.sleep(1.5)
    await xx.edit("WADUH POTO SIAPA YANG DIPAKE!")
    await asyncio.sleep(1.5)
    await xx.edit("PINTEREST YA AWOKAWOK")
    await asyncio.sleep(1.5)
    await xx.edit("KWKWKWKW")
    await asyncio.sleep(1.5)
    await xx.edit("KAGAK PUNYA MUKA")
    await asyncio.sleep(1.5)
    await xx.edit("GW SIH MENDING GA PAKE PP DARI PADA PP WAJAH ORANG LAIN WKWKW")
    await asyncio.sleep(1.5)
    await xx.edit("NORAK!!")
    await asyncio.sleep(1.5)
    await xx.edit("LARI ADA FAKERRRR!")


@HIRO.UBOT("nyanyi")
async def toxicnyanyi(ubot: ubot, message: Message):
    user_id = await extract_user(message)
    if user_id in DEVS:
        return await edit_or_reply(
            message, "**Perintah ini Dilarang digunakan Kepada Developer Saya**"
        )
    xx = await edit_or_reply(message, "**OOOO**")
    await asyncio.sleep(1.5)
    await xx.edit("**INI NI YG HOBI NYA NYANYI PAS OS?**")
    await asyncio.sleep(1.5)
    await xx.edit("**SUARA KEK MUNGSANG AJA DI KELUARIN**")
    await asyncio.sleep(1.5)
    await xx.edit("**GA MALU APA 🗿?**")
    await asyncio.sleep(1.5)
    await xx.edit("**NI INGET**")
    await asyncio.sleep(1.5)
    await xx.edit("**LU KALAU MAU NYANYI**")
    await asyncio.sleep(1.5)
    await xx.edit("**MENDING JANGAN NYANYI SANA SINI GBLK**")
    await asyncio.sleep(1.5)
    await xx.edit("**MENDING LU NYANYI SENDIRI AJA GOBLOK**")
    await asyncio.sleep(1.5)
    await xx.edit("**JANGAN NYANYI DEKAT GWE JIJIK GWE DENGAR SUARA LU YG GA SEBERAPA ITU!**")



@HIRO.UBOT("yameteh")
async def toxicyameteh(ubot: ubot, message: Message):
    user_id = await extract_user(message)
    if user_id in DEVS:
        return await edit_or_reply(
            message, "**Perintah ini Dilarang digunakan Kepada Developer Saya**"
        )
    xx = await edit_or_reply(message, "OI OII YAMETEH")
    await asyncio.sleep(1.5)
    await xx.edit("GA KEREN LU BEGITU")
    await asyncio.sleep(1.5)
    await xx.edit("YAMETEH YAMETEH APAAN DAH")
    await asyncio.sleep(1.5)
    await xx.edit("GETAL?")
    await asyncio.sleep(1.5)
    await xx.edit("YAMETEH MULU DISEBUT GA ADA YANG LAIN")
    await asyncio.sleep(1.5)
    await xx.edit("GATEL BERKEDOK YAMETEH")
    await asyncio.sleep(1.5)
    await xx.edit("AH YAMETEH")
    await asyncio.sleep(1.5)
    await xx.edit("BHAHAHAHA")
    await asyncio.sleep(1.5)
    await xx.edit("YAMETEH AJA AMPE MENINGGAL")
    


@HIRO.UBOT("p")
async def toxicp(ubot: ubot, message: Message):
    user_id = await extract_user(message)
    if user_id in DEVS:
        return await edit_or_reply(
            message, "**Perintah ini Dilarang digunakan Kepada Developer Saya**"
        )
    xx = await edit_or_reply(message, "pa pe pa pe")
    await asyncio.sleep(1.5)
    await xx.edit("coba ngomong jelas sedikit")
    await asyncio.sleep(1.5)
    await xx.edit("assalamualaikum kek apa kek")
    await asyncio.sleep(1.5)
    await xx.edit("ini pa pe pa pe")
    await asyncio.sleep(1.5)
    await xx.edit("p aja sendiri")
    await asyncio.sleep(1.5)
    await xx.edit("maka nya luh itu di kacangin")
    await asyncio.sleep(1.5)
    await xx.edit("sadar kalau ngetik!!!")
    await asyncio.sleep(1.5)
    await xx.edit("APA MAU P LAGI?")
    await asyncio.sleep(1.5)
    await xx.edit("SINI KEPALA KAU KU P PAKE KAKI")
  
