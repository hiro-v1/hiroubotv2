import requests
import wget
import os
import glob
from pyrogram import filters
from DanteUserbot import *
from pyrogram.errors.exceptions.bad_request_400 import MediaInvalid
from pyrogram.types import Message, InputMediaPhoto
import asyncio
from pyrogram.raw.functions.messages import DeleteHistory


__MODULE__ = "ᴘɪɴᴛ"
__HELP__ = """
**--Pinterest--**

<blockquote><b>
  • perintah: {0}.pint jumlah kata_kunci
  • penjelasan: untuk mengunduh media tanpa link di pinterest.

  • Perintah: {0}.pintlink tautan link pinterest 
  • Penjelasan: Untuk mengunduh media dari pinterest.
</b></blockquote>"""

@DANTE.UBOT("pint")
async def pinterest(client, message):
    chat_id = message.chat.id

    if len(message.command) < 3:
        return await message.reply("Gunakan .pint jumlah kata_kunci")

    msg = await message.reply("🔍Sedang mencari...")

    try:
        jumlah = int(message.command[1])
        query = ' '.join(message.command[2:])
    except (IndexError, ValueError):
        return await msg.edit("❌ Salin url dari pinterest dan ketik .pint jumlah kata_kunci 🔍")

    try:
        response = requests.get(f"https://pinterest-api-one.vercel.app/?q={query}")
        response.raise_for_status()
    except requests.RequestException as e:
        return await msg.edit(f"Gagal mengambil data dari API: {e}")

    images = response.json().get("images", [])
    if not images:
        return await msg.edit("Tidak ada gambar yang ditemukan.")

    media_group = []
    for url in images[:jumlah]:
        try:
            image_response = requests.get(url, stream=True)
            if image_response.status_code == 200:
                potonya = wget.download(url)
                media_group.append(InputMediaPhoto(media=potonya))
            else:
                await message.reply(f"URL tidak dapat dijangkau: {url}")
        except requests.RequestException as e:
            await msg.edit(f"Gagal mengakses URL: {url} - Error: {e}")

    if media_group:
        try:
            await client.send_media_group(chat_id, media_group)
        except MediaInvalid:
            for meki in images[:jumlah]:
                try:
                    await client.send_photo(chat_id, meki)
                except:
                    pass
        except Exception as e:
            await msg.edit(f"Gagal mengirim media: {e}")
    else:
        await msg.edit("Tidak ada media yang valid untuk dikirim.")

    await msg.delete()
    try:
        os.system("rm -rf *.jpg")
    except Exception as e:
        print(f"Error removing file {file_path}: {e}")

@DANTE.UBOT("pintlink")
async def _(client, message):
    if len(message.command) < 2:
        return
    Tm = await eor(message, "<code>Processing . . .</code>")
    link = message.text.split()[1]
    bot = "SaveAsbot"
    await client.unblock_user(bot)
    await client.send_message(bot, link)
    # await xnxx.delete()
    await asyncio.sleep(8)
    async for sosmed in client.search_messages(bot):
        try:
            if sosmed.video:
                await sosmed.copy(
                    message.chat.id,
                    caption=f"<b>Upload By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
                    reply_to_message_id=message.id,
                )
            else:
                try:
                    if sosmed.photo:
                        await sosmed.copy(
                            message.chat.id,
                            caption=f"<b>Upload By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
                            reply_to_message_id=message.id,
                        )
                        await Tm.delete()
                except Exception:
                    await Tm.edit(
                        "<b>Video tidak ditemukan silahkan ulangi beberapa saat lagi</b>"
                    )
        except Exception:
            pass
    user_info = await client.resolve_peer(bot)
    return await client.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))
