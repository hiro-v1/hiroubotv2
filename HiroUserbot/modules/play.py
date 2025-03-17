import os
import re
import asyncio
from pyrogram.types import Message
from pytgcalls import filters as fl
from pytgcalls import PyTgCalls
from pytgcalls.types import ChatUpdate
from pytgcalls.types import GroupCallParticipant
from pytgcalls.types import MediaStream
from pytgcalls.types import AudioQuality
from pytgcalls.types import MediaStream
from pytgcalls.types import VideoQuality
from pytgcalls.types import Update
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from functools import partial
from HiroUserbot import *
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

mycookies = "usup_cok.txt"

def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r['id']
            if len(r['title']) > 34:
                songname = r['title'][:35] + "..."
            else:
                songname = r['title']
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def run_sync(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    p_func = partial(func, *args, **kwargs)
    return await loop.run_in_executor(None, p_func)


async def YoutubeDownload(url, as_video=False):
    if as_video:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
            "cookiefile": mycookies,
        }
    else:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
            "cookiefile": mycookies,
        }
    data_ytp = "<b>🗯 ɪɴꜰᴏʀᴍᴀsɪ {}</b>\n\n<b>💠 ɴᴀᴍᴀ:</ʙ> {}<b>\n<b>⏲ ᴅᴜʀᴀsɪ:</b> {}\n<b>🎑 ᴅɪʟɪʜᴀᴛ:</b> {}\n<b>🌍 ᴄʜᴀɴɴᴇʟ:</b> {}\n<b>🔗 ᴛᴀᴜᴛᴀɴ:</b> <a href={}>ʏᴏᴜᴛᴜʙᴇ</a>\n\n<b> ᴘʟᴀʏ ʙʏ :</b> {}"
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


@HIRO.UBOT("play")
@HIRO.GROUP
async def play(client, m: Message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    replied = m.reply_to_message
    chat_id = m.chat.id
    if replied:
        if replied.audio or replied.voice:
            huehue = await replied.reply(f"{brhsl}<b>ᴘʀᴏᴄᴄᴇsɪɴɢ...</b>")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:35] + "..."
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.edit(f"<b>{brhsl}ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴀɴᴛʀɪᴀɴ #{pos}</b>")
            else:
                try:
                    await client.call_py.play(
                        chat_id,
                        MediaStream(
                        dl,
                        AudioQuality.STUDIO,
                        ),
                    )
                    add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                    await huehue.edit(f"**<emoji id=5895705279416241926>▶</emoji> sᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ ᴀᴜᴅɪᴏ** \n**<emoji id=6026256492619895014>🎵</emoji> ɴᴀᴍᴇ** : [{songname}]({link}) \n**<emoji id=5323442290708985472>©</emoji> ᴄʜᴀᴛ** : `{chat_id}`", disable_web_page_preview=True)
                    os.remove(dl)
                except Exception as hmme:
                    await huehue.edit(hmme)
        else:
            if len(m.command) < 2:
                await m.reply(f"<b>{ggl}ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ᴀᴜᴅɪᴏ ғɪʟᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇᴛʜɪɴɢ ᴛᴏ sᴇᴀʀᴄʜ</b>")
            else:
                huehue = await m.reply("`Getting...`")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await huehue.edit(f"{ggl}<b>ғᴏᴜɴᴅ ɴᴏᴛʜɪɴɢ ғᴏʀ ᴛʜᴇ ɢɪᴠᴇɴ ǫᴜᴇʀʏ !</b>")
                else:
                    songname = search[0]
                    url = search[1]
                    try:
                        file_name, title, yt_url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(url)
                        if chat_id in QUEUE:
                            pos = add_to_queue(chat_id, songname, file_name, yt_url, "Audio", 0)
                            await huehue.edit(f"<b>{brhsl}ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴀɴᴛʀɪᴀɴ #{pos}</b>")
                        else:
                            try:
                                await client.call_py.play(
                                    chat_id,
                                    MediaStream(
                                    file_name,
                                    AudioQuality.STUDIO,
                                    ),
                                )                                
                                add_to_queue(chat_id, songname, file_name, yt_url, "Audio", 0)
                                await huehue.edit(f"**<emoji id=5895705279416241926>▶</emoji> sᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ ᴀᴜᴅɪᴏ** \n**<emoji id=6026256492619895014>🎵</emoji> sᴏɴɢ** : [{songname}]({url}) \n**<emoji id=5323442290708985472>©</emoji> ᴄʜᴀᴛ** : `{chat_id}`", disable_web_page_preview=True)
                                os.remove(file_name)
                            except Exception as ep:
                                await huehue.edit(f"`{ep}`")
                    except Exception as e:
                        await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{str(e)}`")
    else:
        if len(m.command) < 2:
            await m.reply(f"{ggl}<b>ᴍᴏʜᴏɴ ʙᴀʟᴀs ᴋᴇ ᴀᴜᴅɪᴏ ᴀᴛᴀᴜ ᴋᴇᴛɪᴋ</b> <code>play judul lagu</code>")
        else:
            huehue = await m.reply(f"{prs}<b>sᴇᴀʀᴄʜɪɴɢ...</b>")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit(f"{ggl}<b>ғᴏᴜɴᴅ ɴᴏᴛʜɪɴɢ ғᴏʀ ᴛʜᴇ ɢɪᴠᴇɴ ǫᴜᴇʀʏ !</b>")
            else:
                songname = search[0]
                url = search[1]
                try:
                    file_name, title, yt_url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(url)
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, file_name, yt_url, "Audio", 0)
                        await huehue.edit(f"<b>{brhsl}ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴀɴᴛʀɪᴀɴ #{pos}</b>")
                    else:
                        try:
                            await client.call_py.play(
                                chat_id,
                                MediaStream(
                                file_name,
                                AudioQuality.STUDIO,
                                ),
                            )
                            add_to_queue(chat_id, songname, file_name, yt_url, "Audio", 0)
                            await huehue.edit(f"**<emoji id=5895705279416241926>▶</emoji>sᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ ᴀᴜᴅɪᴏ** \n**<emoji id=6026256492619895014>🎵</emoji> sᴏɴɢ** : [{songname}]({url}) \n**<emoji id=5323442290708985472>©</emoji> ᴄʜᴀᴛ** : `{chat_id}`", disable_web_page_preview=True)
                            os.remove(file_name)
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")
                except Exception as e:
                    await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{str(e)}`")
