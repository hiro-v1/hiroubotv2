from pyrogram import filters, Client
from pyrogram.types import Message
from DanteUserbot import *

__MODULE__ = "ᴀᴜᴛᴏsᴄʀᴏʟʟ"
__HELP__ = f"""
<blockquote>
**Perintah:** `autoscroll`
• **Fungsi:** Kirim gulir otomatis di obrolan apa pun untuk secara otomatis membaca semua pesan terkirim hingga Anda menelepon
gulir otomatis lagi. Ini berguna jika Anda membuka Telegram di layar lain.
</blockquote>"""
f = filters.chat([])

if f:
    @Client.on_message(f)
    async def auto_read(bot: Client, message: Message):
        await bot.read_history(message.chat.id)
        message.continue_propagation()

@DANTE.UBOT("scroll")
async def add_to_auto_read(bot: Client, message: Message):
    if message.chat.id in f:
        f.remove(message.chat.id)
        await message.edit("Autoscroll deactivated")
    else:
        f.add(message.chat.id)
        await message.edit("Autoscroll activated")
