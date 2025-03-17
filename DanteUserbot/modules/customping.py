from DanteUserbot import *
from DanteUserbot.core.helpers.emoji import EMO

__MODULE__ = "sᴇᴛᴘɪɴɢ"
__HELP__ = """
**--Bantuan untuk mengubah tampilan emoji ping--**
<blockquote>
note: hanya pengguna akun telegram premium yang bisa menggunakan ini.

perintah : <code>.emoji</code> query emoji prem
   untuk merubah emoji pada tampilan tertentu

query:
    <code>ping</code>
    <code>owner</code>
    <code>ubot</code>
    
contoh :
.emoji ping (gunakan emot prem disini)
.emoji owner (gunakan emot prem disini)
.emoji ubot (gunakan emot prem disini)
</blockquote>
"""

@DANTE.UBOT("emoji")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    try:
        msg = await message.reply(f"{prs}memproses...", quote=True)

        if not client.me.is_premium:
            return await msg.edit(
                f"{ggl}beli prem dulu jika ingin menggunakan emoji"
            )

        if len(message.command) < 3:
            return await msg.edit(f"{ggl}tolong masukkan query dan valuenya")

        query_mapping = {
            "ping": "EMOJI_PING",
            "owner": "EMOJI_MENTION",
            "ubot": "EMOJI_USERBOT",
        }
        command, mapping, value = message.command[:3]

        if mapping.lower() in query_mapping:
            query_var = query_mapping[mapping.lower()]
            emoji_id = None
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break

            if emoji_id:
                await set_vars(client.me.id, query_var, emoji_id)
                await msg.edit(
                    f"{brhsl}emoji berhasil di setting ke: <emoji id={emoji_id}>{value}</emoji>"
                )
            else:
                await msg.edit(f"{ggl}tidak dapat menemukan emoji premium")
        else:
            await msg.edit(f"{ggl}mapping tidak ditemukan")

    except Exception as error:
        await msg.edit(str(error))
