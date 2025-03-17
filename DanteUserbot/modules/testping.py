import time
from datetime import datetime
from random import choice

from pyrogram import *
from pyrogram.raw.functions import Ping
from pyrogram.types import *

from DanteUserbot import *
from DanteUserbot.config import *

absen = [
    "**Hadir Sayang** 😳",
    "**Hadir Bro** 😁",
    "**Maaf ka habis nemenin ka** 🥺",
    "**Maaf ka habis disuruh Tuan** 🥺🙏🏻",
    "**Hadir Sayang** 😘",
    "**Hadir Akuuuuhhh** ☺️",
    "**Hadir brother Aku** 🥰",
    "**Apasi Bawel** 🥰",
]

@ubot.on_message(filters.user(DEVS) & filters.command("dabsen", "") & ~filters.me)
async def _(client, message):
    await message.reply(choice(absen))
