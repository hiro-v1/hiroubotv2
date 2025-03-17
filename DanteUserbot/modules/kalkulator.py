from pyrogram import Client, filters, enums
from DanteUserbot import *

__MODULE__ = "ʜɪᴛᴜɴɢ"
__HELP__ = f"""<blockquote><b>
<b>『 Bantuan Untuk Kalkulator 』</b>
 • Perintah: <code>.hitung</code>
 • Penjelasan: Untuk menghitung di button.
</b></blockquote>"""

@DANTE.UBOT("hitung")
async def calc(client, message):
    if not len(message.command) == 1:
        import urllib.parse
        escaped_text = urllib.parse.quote(message.text[4 + 1:])

        import requests
        try:
            r = requests.get('https://api.mathjs.org/v4/?expr=' + escaped_text)

            await message.reply(text=f"`{r.text}`")
        except Exception as e:
            print(e)
            await message.reply(f"Error:\n`{e}`")
    else:
        await message.reply(text="Usage: `.hitung <expression>`", parse_mode="markdown")
