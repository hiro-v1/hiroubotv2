import asyncio
import re
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import VideoPiped

from DanteUserbot import *
from DanteUserbot.core.helpers.client import bot

# Simpan daftar playlist
PLAYLIST = {}

# Regex untuk cek apakah link Telegram valid
TELEGRAM_LINK_PATTERN = r"(https?://)?(t\.me|telegram\.me)/([a-zA-Z0-9_]+)/(\d+)?"


async def get_video_from_link(client, link):
    """Mengambil video dari channel/grup berdasarkan link."""
    match = re.search(TELEGRAM_LINK_PATTERN, link)
    if not match:
        return None, "❌ Link tidak valid!"

    username = match.group(3)  # Username channel atau grup
    message_id = match.group(4)  # ID pesan jika ada

    # Ambil ID channel/group
    try:
        chat = await client.get_chat(username)
        chat_id = chat.id
    except Exception:
        return None, "❌ Gagal mendapatkan channel/grup!"

    # Ambil video dari pesan yang diberikan
    try:
        if message_id:
            video_message = await client.get_messages(chat_id, int(message_id))
        else:
            video_message = await client.get_history(chat_id, limit=1)  # Ambil pesan terbaru

        if not video_message.video:
            return None, "❌ Tidak ada video dalam pesan ini!"
        return video_message.video.file_id, None
    except Exception as e:
        return None, f"❌ Gagal mengambil video: {e}"


@DANTE.UBOT("chplay")
async def chplay(client: Client, message: Message):
    """Memutar video dari channel/grup berdasarkan link."""
    if len(message.command) < 2:
        return await message.reply("⚠️ **Masukkan link video dari channel/grup!**")

    link = message.command[1]
    await message.reply("🎥 **Mengambil video...**")

    video_file_id, error_msg = await get_video_from_link(client, link)
    if error_msg:
        return await message.reply(error_msg)

    chat_id = message.chat.id

    # Tambahkan ke playlist
    if chat_id not in PLAYLIST:
        PLAYLIST[chat_id] = []
    PLAYLIST[chat_id].append(video_file_id)

    # Jika tidak ada yang sedang diputar, mulai memutar
    if len(PLAYLIST[chat_id]) == 1:
        await play_next_video(client, chat_id)

    await message.reply(f"▶ **Menambahkan ke playlist:** {link} 🎶")


async def play_next_video(client, chat_id):
    """Memutar video berikutnya dari playlist."""
    if chat_id not in PLAYLIST or not PLAYLIST[chat_id]:
        return

    video_file_id = PLAYLIST[chat_id].pop(0)

    try:
        await client.call_py.join_group_call(
            chat_id,
            VideoPiped(video_file_id),
            stream_type=StreamType().pulse_stream,
        )
        await bot.send_message(chat_id, "🎬 **Memutar video berikutnya...**")
    except Exception as e:
        await bot.send_message(chat_id, f"❌ **Gagal memutar video:** {e}")


@DANTE.UBOT("stopcp")
async def stopcp(client: Client, message: Message):
    """Menghentikan video yang sedang diputar dan menghapus playlist."""
    chat_id = message.chat.id

    try:
        await client.call_py.leave_group_call(chat_id)
        PLAYLIST[chat_id] = []  # Hapus playlist
        await message.reply("🛑 **Video dihentikan dan playlist dikosongkan!**")
    except Exception as e:
        await message.reply(f"❌ **Gagal menghentikan video:** {e}")

__MODULE__ = "chply"
__HELP__ = """ 🎬 -- PANDUAN PENGGUNAAN chplay --
<blockquote><b> ✅ **Perintah:** <code>{0}chplay</code> [link_channel] 
🔹 **Penjelasan:** Memutar video dari **channel/grup** di obrolan suara.
✅ Perintah: <code>{0}stopcp</code>
🔹 Penjelasan: Menghentikan video yang sedang diputar dan menghapus playlist.

🚀 Contoh Penggunaan:
➜ <code>.chplay https://t.me/nama_channel/1234</code>
➜ <code>.stopcp</code>

</b></blockquote>
"""

