import os
import requests
from asyncio import Queue
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls.group_call_factory import GroupCallFactory
from DanteUserbot import *

# Menggunakan sesi utama DanteUserbot
group_call_factory = GroupCallFactory(ubot)
group_call = group_call_factory.get_file_group_call()
queue = Queue()

# Fungsi untuk mendapatkan URL Video
def get_url(platform, video_id):
    """Mendapatkan URL video dari Vimeo atau DailyMotion"""
    try:
        if platform == "vimeo":
            api_url = f"https://vimeo.com/api/v2/video/{video_id}.json"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return data[0]['download'][0]['link']  # Mendapatkan URL unduhan

        elif platform == "dailymotion":
            api_url = f"https://api.dailymotion.com/video/{video_id}?fields=stream_hls"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return data['stream_hls']  # Mendapatkan URL HLS
    except Exception:
        pass

    raise ValueError(f"❌ Gagal mendapatkan URL {platform.capitalize()}.")

# Fungsi untuk memutar video
async def play_video(client: Client, message: Message, platform: str):
    """Fungsi umum untuk memutar video dari Vimeo atau DailyMotion"""
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)

    if len(message.command) < 2:
        return await message.reply_text(f"{ggl} Gunakan: <code>{message.command[0]} <video_id></code>")

    video_id = message.command[1]
    chat_id = message.chat.id
    loading_msg = await message.reply_text(f"{prs} Mengambil video...")

    try:
        video_url = get_url(platform, video_id)

        if queue.empty():
            await group_call.start(chat_id)
            await group_call.input_video_stream(video_url)
            await loading_msg.edit(f"{sks} Sedang memutar video {platform.capitalize()}: `{video_id}`")
        else:
            await queue.put((chat_id, video_url, video_id))
            await loading_msg.edit(f"🎵 Video ditambahkan ke antrian.")
    except Exception as e:
        await loading_msg.edit(f"{ggl} Terjadi kesalahan: `{str(e)}`")

# Perintah untuk memutar video dari Vimeo
@DANTE.UBOT("playvimeo")
@DANTE.GROUP
async def play_vimeo(client: Client, message: Message):
    await play_video(client, message, "vimeo")

# Perintah untuk memutar video dari DailyMotion
@DANTE.UBOT("dmplay")
@DANTE.GROUP
async def play_dailymotion(client: Client, message: Message):
    await play_video(client, message, "dailymotion")

# Perintah untuk melihat antrian pemutaran
@DANTE.UBOT("queue")
@DANTE.GROUP
async def view_queue(client: Client, message: Message):
    if queue.empty():
        return await message.reply_text("📭 **Antrian kosong!**")
    
    queue_list = list(queue._queue)  # Mendapatkan daftar antrian
    text = "**🎶 Daftar Antrian:**\n"
    
    for index, (chat_id, _, video_id) in enumerate(queue_list, start=1):
        text += f"{index}. `{video_id}`\n"

    await message.reply_text(text)

# Perintah untuk melewati lagu
@DANTE.UBOT("skip")
@DANTE.GROUP
async def skip_video(client: Client, message: Message):
    if queue.empty():
        return await message.reply_text("📭 **Tidak ada video dalam antrian untuk dilewati!**")

    next_video = queue.get_nowait()
    chat_id, video_url, video_id = next_video

    try:
        await group_call.input_video_stream(video_url)
        await message.reply_text(f"⏭ Melewati ke video berikutnya: `{video_id}`")
    except Exception as e:
        await message.reply_text(f"❌ **Gagal melewati video:** `{str(e)}`")
