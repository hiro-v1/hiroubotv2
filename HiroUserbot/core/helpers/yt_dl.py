from asyncio import get_event_loop
from functools import partial

from yt_dlp import YoutubeDL

mycookies = "usup_cok.txt"

def run_sync(func, *args, **kwargs):
    return get_event_loop().run_in_executor(None, partial(func, *args, **kwargs))


async def YoutubeDownload(url, as_video=False):
    if as_video:
        ydl_opts = {
            "quiet": True,
            "cookiefile": mycookies,
            "no_warnings": True,
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    else:
        ydl_opts = {
            "quiet": True,
            "cookiefile": mycookies,
            "no_warnings": True,
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    data_ytp = "<b><emoji id=5224596414415256150>💡</emoji> informasi {}</b>\n\n<b><emoji id=5904544038643569182>🏷</emoji> nama:</b> {}<b>\n<b><emoji id=6030547358222127917>🧭</emoji> durasi:</b> {}\n<b><emoji id=5233246225146332642>👀</emoji> dilihat:</b> {}\n<b><emoji id=5891268505185030578>📢</emoji> channel:</b> {}\n<b><emoji id=5271604874419647061>🔗</emoji> tautan:</b> <a href={}>youtube</a>\n\n<b><emoji id=5801170880272797821>⚡</emoji> powered by:</b> {}"
    ydl = YoutubeDL(ydl_opts)
    ytdl_data = await run_sync(ydl.extract_info, url, download=True)
    file_name = ydl.prepare_filename(ytdl_data)
    videoid = ytdl_data["id"]
    title = ytdl_data["title"]
    url = f"https://youtu.be/{videoid}"
    duration = ytdl_data["duration"]
    channel = ytdl_data["uploader"]
    views = f"{ytdl_data['view_count']:,}".replace(",", ".")
    thumb = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    return file_name, title, url, duration, views, channel, thumb, data_ytp
