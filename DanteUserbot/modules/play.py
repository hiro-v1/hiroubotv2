import os
import re
import asyncio
from pyrogram.types import Message
from pytgcalls import filters as fl
from pytgcalls import PyTgCalls
from pytgcalls.types import ChatUpdate
from pytgcalls.types import GroupCallParticipant
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality
from pytgcalls.types import Update
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from functools import partial
from DanteUserbot import *
from collections import deque
import time

__MODULE__ = "ᴍᴜsɪᴄ"
__HELP__ = """<blockquote><b>
cmd : <code>{0}play</code>
    untuk memutar music

cmd : <code>{0}end</code>
    untuk menghentikan music

cmd : <code>{0}skip</code>
    untuk mengskip music

cmd : <code>{0}pause</code>
    untuk menjeda music

cmd : <code>{0}resume</code>
    untuk menjeda music</b></blockquote>
"""

# 📌 Mencari Video di YouTube
async def ytsearch(query, limit=1):
    """Mencari video YouTube berdasarkan query."""
    try:
        search = VideosSearch(query, limit=limit)
        results = search.result().get("result", [])

        if not results:
            return None  # Tidak ditemukan

        videos = []
        for result in results:
            video_id = result["id"]
            title = result["title"]
            duration = result.get("duration", "Unknown Duration")
            url = f"https://www.youtube.com/watch?v={video_id}"

            videos.append({
                "title": title,
                "url": url,
                "duration": duration
            })

        return videos

    except Exception as e:
        print(f"⚠️ Error saat mencari video: {e}")
        return None  # Hindari crash jika terjadi error

YOUTUBE_COOKIES = "usup_cok.txt"

async def run_sync(func, *args, **kwargs):
    """Jalankan fungsi secara sinkron di dalam event loop."""
    loop = asyncio.get_event_loop()
    p_func = partial(func, *args, **kwargs)
    return await loop.run_in_executor(None, p_func)

async def yt_download(url, as_video=False):
    """Mengunduh audio/video dari YouTube menggunakan yt-dlp."""
    cookies_file = check_cookies()  # Cek cookies sebelum digunakan

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best" if not as_video else "(bestvideo[height<=?720][ext=mp4])+bestaudio[ext=m4a]",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "noprogress": True,  # Menghindari timeout karena progress
        "retries": 5,  # Coba ulang hingga 5 kali jika gagal
        "fragment-retries": 10,  # Coba ulang fragmen jika gagal
        "socket-timeout": 15,  # Timeout 15 detik untuk koneksi lambat
        "concurrent-fragments": 5,  # Unduh dengan 5 fragmen sekaligus
        "writethumbnail": True,  # Simpan thumbnail
        "nocheckcertificate": True,
        "geo_bypass": True,
        **({"cookiefile": cookies_file} if cookies_file else {}),  # Gunakan cookies jika tersedia
    }

    ydl = YoutubeDL(ydl_opts)

    try:
        ytdl_data = await run_sync(ydl.extract_info, url, download=True)
        file_name = ydl.prepare_filename(ytdl_data)
        return {
            "file": file_name,
            "title": ytdl_data["title"],
            "url": f"https://youtu.be/{ytdl_data['id']}",
            "duration": ytdl_data["duration"],
            "views": f"{ytdl_data['view_count']:,}".replace(",", "."),
            "channel": ytdl_data["uploader"],
            "thumb": f"https://img.youtube.com/vi/{ytdl_data['id']}/hqdefault.jpg",
        }
    except Exception as e:
        raise ValueError(f"❌ Gagal mengunduh video: {str(e)}")

def is_cookies_valid(cookie_file):
    """Cek apakah cookies YouTube masih valid dengan mencoba akses halaman YouTube."""
    if not os.path.exists(cookie_file):
        print("❌ Cookies tidak ditemukan! Harap unggah ulang file cookies.")
        return False

    try:
        test_url = "https://www.youtube.com"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }
        cookies = {}

        # Membaca cookies dari file
        with open(cookie_file, "r") as f:
            for line in f:
                if not line.startswith("#"):
                    parts = line.strip().split("\t")
                    if len(parts) >= 7:
                        cookies[parts[5]] = parts[6]

        response = requests.get(test_url, headers=headers, cookies=cookies, timeout=5)

        if response.status_code == 200:
            print("✅ Cookies valid! Menggunakan cookies untuk YouTube.")
            return True
        else:
            print(f"⚠️ Cookies mungkin sudah kadaluarsa! (Status Code: {response.status_code})")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Gagal memverifikasi cookies: {str(e)}")
        return False

def check_cookies():
    """Memastikan cookies tersedia dan valid sebelum digunakan."""
    if is_cookies_valid(YOUTUBE_COOKIES):
        return YOUTUBE_COOKIES
    else:
        print("⚠️ Cookies tidak valid atau kadaluarsa! Menggunakan mode tanpa cookies.")
        return None  # Jangan gunakan cookies jika tidak valid

YDL_OPTS_AUDIO = {
    "quiet": True,
    "no_warnings": True,
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(id)s.%(ext)s",
    "nocheckcertificate": True,
    "geo_bypass": True,
    **({"cookiefile": check_cookies()} if check_cookies() else {}),  # Gunakan cookies hanya jika valid
    "proxy": "socks5://127.0.0.1:9050",  # Gunakan proxy jika diperlukan
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
    "http_headers": {
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    },
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "external_downloader": "aria2c",
    "external_downloader_args": ["-x", "16", "-s", "16", "-k", "1M"]
}

YDL_OPTS_VIDEO = {
    "quiet": True,
    "no_warnings": True,
    "format": "(bestvideo[height<=?720][ext=mp4])+bestaudio[ext=m4a]",
    "outtmpl": "downloads/%(id)s.%(ext)s",
    "nocheckcertificate": True,
    "geo_bypass": True,
    **({"cookiefile": check_cookies()} if check_cookies() else {}),  # Gunakan cookies hanya jika valid
    "proxy": "socks5://127.0.0.1:9050",  # Gunakan proxy jika diperlukan
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
    "external_downloader": "aria2c",
    "external_downloader_args": ["-x", "16", "-s", "16", "-k", "1M"]
}

from asyncio import Queue

# Membuat antrian global
QUEUE = {}

def get_queue(chat_id):
    """Mengembalikan daftar lagu/video dalam antrian."""
    if chat_id in QUEUE and not QUEUE[chat_id].empty():
        return list(QUEUE[chat_id]._queue)
    return []

def clear_queue(chat_id):
    """Menghapus semua lagu/video dalam antrian."""
    if chat_id in QUEUE:
        QUEUE[chat_id] = Queue()

def add_to_queue(chat_id, name, file_path, yt_url, media_type, duration):
    """Menambahkan lagu/video ke dalam antrian."""
    if chat_id not in QUEUE:
        QUEUE[chat_id] = Queue()

    media_data = {
        "name": name,
        "path": file_path,
        "url": yt_url,
        "type": media_type,
        "duration": duration
    }

    QUEUE[chat_id].put_nowait(media_data)
    return QUEUE[chat_id].qsize()  # Mengembalikan posisi dalam antrian
    
async def play_audio(chat_id, file_name):
    """Memutar audio dengan kualitas terbaik yang tetap stabil."""
    try:
        await ubot.call_py.play(
            chat_id,
            MediaStream(
                file_name,
                AudioQuality.HIGH,  # Gunakan kualitas tinggi yang tetap stabil
            ),
        )
    except Exception as e:
        raise ValueError(f"❌ Gagal memutar audio: {str(e)}")

async def play_video(chat_id, file_name):
    """Memutar video dengan kualitas 720p agar tetap stabil."""
    try:
        await ubot.call_py.play(
            chat_id,
            MediaStream(
                file_name,
                VideoQuality.Q720P,  # 720p agar tetap lancar tanpa buffering
            ),
        )
    except Exception as e:
        raise ValueError(f"❌ Gagal memutar video: {str(e)}")
        
async def play_with_buffer(chat_id, file_name, is_video=False):
    """Memuat file lebih dulu untuk mencegah buffering sebelum diputar."""
    buffering_msg = await ubot.send_message(chat_id, "⏳ **Menyiapkan pemutaran...**")
    
    # Tambahkan delay kecil untuk memastikan file siap diputar
    time.sleep(2)  

    try:
        if is_video:
            await play_video(chat_id, file_name)
        else:
            await play_audio(chat_id, file_name)
        
        await buffering_msg.edit("🎵 **Sedang diputar...**")
    except Exception as e:
        await buffering_msg.edit(f"❌ **Gagal memutar:** {str(e)}") 

@DANTE.UBOT("vplay")
@DANTE.GROUP
async def vplay(client, message: Message):
    """Memutar video dari YouTube di grup chat."""
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)

    chat_id = message.chat.id
    query = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    if not query:
        return await message.reply(f"{ggl} Mohon masukkan judul atau URL video YouTube!")

    huehue = await message.reply(f"{prs} Sedang mencari video...")

    search_results = await ytsearch(query)
    if not search_results or len(search_results) == 0:
        return await huehue.edit(f"{ggl} Tidak menemukan hasil untuk {query}")

    video = search_results[0]  # Ambil hasil pertama
    yt_url = video["url"]
    video_title = video["title"]

    try:
        await huehue.edit(f"⏳ **Mengunduh video...**")

        dl_result = await yt_download(yt_url, as_video=True)
        if not dl_result:
            return await huehue.edit(f"{ggl} Gagal mengunduh video!")

        file_path = dl_result["file"]

        if chat_id in QUEUE and not QUEUE[chat_id].empty():
            pos = add_to_queue(chat_id, video_title, file_path, yt_url, "Video", dl_result["duration"])
            return await huehue.edit(f"📽 **Video Ditambahkan ke Antrian** #{pos} \n🎥 **Judul:** [{video_title}]({yt_url})")

        await huehue.edit(f"🎥 **Memulai pemutaran video...**")

        await client.call_py.play(
            chat_id,
            MediaStream(
                file_path,
                VideoQuality.Q720P,  # 720p untuk menjaga kestabilan
            ),
        )

        add_to_queue(chat_id, video_title, file_path, yt_url, "Video", dl_result["duration"])

        await huehue.edit(
            f"{brhsl} **HiroUbot Sedang Memutar 🎥**\n"
            f"📽 **Video:** [{video_title}]({yt_url})\n"
            f"🎧 **Grup:** `{chat_id}`",
            disable_web_page_preview=True,
        )

    except Exception as e:
        await huehue.edit(f"{ggl} Terjadi kesalahan: `{str(e)}`")


@DANTE.UBOT("play")
@DANTE.GROUP
async def play(client, message: Message):
    """Memutar lagu di grup dari YouTube"""
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)

    chat_id = message.chat.id
    query = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    if not query:
        return await message.reply(f"{ggl} Mohon masukkan judul lagu!")

    huehue = await message.reply(f"{prs} Sedang mencari lagu...")

    search_results = await ytsearch(query)
    if not search_results:
        return await huehue.edit(f"{ggl} Tidak menemukan hasil untuk {query}")

    video = search_results[0]  # Ambil hasil pertama
    yt_url = video["url"]
    songname = video["title"]

    try:
        dl_result = await yt_download(yt_url)
        if not dl_result:
            return await huehue.edit(f"{ggl} Gagal mengunduh lagu!")

        file_path = dl_result["file"]

        if chat_id in QUEUE and not QUEUE[chat_id].empty():
            pos = add_to_queue(chat_id, songname, file_path, yt_url, "Audio", dl_result["duration"])
            return await huehue.edit(f"🎵 **Lagu Ditambahkan ke Antrian** #{pos} \n🎶 **Judul:** [{songname}]({yt_url})")

        # Jika antrian kosong, mainkan lagu
        await client.call_py.play(
            chat_id,
            MediaStream(
                file_path,
                AudioQuality.STUDIO,
            ),
        )

        # Tambahkan ke antrian
        add_to_queue(chat_id, songname, file_path, yt_url, "Audio", dl_result["duration"])

        await huehue.edit(
            f"{brhsl} **HiroUbot Sedang Memutar 🎶**\n"
            f"🎵 **Lagu:** [{songname}]({yt_url})\n"
            f"🎧 **Grup:** `{chat_id}`",
            disable_web_page_preview=True,
        )

    except Exception as e:
        await huehue.edit(f"{ggl} Terjadi kesalahan: `{str(e)}`")
        
@DANTE.UBOT("end")
@DANTE.GROUP
async def stop(client, message: Message):
    """Menghentikan semua pemutaran musik/video dan membersihkan antrian."""
    chat_id = message.chat.id
    brhsl = await EMO.BERHASIL(client)

    if chat_id not in QUEUE or QUEUE[chat_id].empty():
        return await message.reply("🚫 Tidak ada musik/video yang sedang diputar.")

    # Ambil media yang sedang diputar jika ada
    current_media = QUEUE.get(chat_id, Queue()).get_nowait() if not QUEUE.get(chat_id, Queue()).empty() else None
    file_path = current_media["path"] if current_media else None

    # Hapus file jika ada
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"⚠️ Gagal menghapus file: {str(e)}")

    # Kosongkan antrian
    QUEUE[chat_id] = Queue()

    # Hanya keluar dari panggilan jika benar-benar kosong
    if QUEUE[chat_id].empty():
        await client.call_py.leave_group_call(chat_id)

    await message.reply(f"{brhsl} Pemutaran dihentikan dan antrian dibersihkan.")

@DANTE.UBOT("skip")
@DANTE.GROUP
async def skip(client, message: Message):
    """Melewati media saat ini dan memainkan berikutnya."""
    chat_id = message.chat.id
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)

    if chat_id not in QUEUE or QUEUE[chat_id].empty():
        return await message.reply(f"{ggl} Tidak ada media dalam antrian!")
