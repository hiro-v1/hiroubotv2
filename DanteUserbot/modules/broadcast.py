import asyncio
import os
import random
from telegraph import upload_file
from pyrogram.types import InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent

from gc import get_objects
from asyncio import sleep
from pyrogram.raw.functions.messages import DeleteHistory, StartBot
from pyrogram.enums import ChatType
from pyrogram import *
from pyrogram.types import *
from pyrogram.errors.exceptions import FloodWait
from pyrogram.errors import FloodWait, ChannelPrivate
from DanteUserbot import *
from DanteUserbot.core.helpers.emoji import
from DanteUserbot.core.database.bcast import (
    is_blacklisted,
    add_blacklist,
    remove_blacklist,
    get_blacklist,
    clear_blacklist,
    set_autogikes,
    get_autogikes,
    remove_autogikes
)

__MODULE__ = "ɢᴄᴀsᴛ"
__HELP__ = """
**--Bantuan untuk Broadcast--**

<b>Perintah utama:</b>
- <code>{0}gcast</code>: Broadcast ke semua grup.
- <code>{0}ucast</code>: Broadcast ke semua user.
- <code>{0}send [target]</code>: Kirim pesan ke user/group/channel (opsional: <code>send user</code>, <code>send group</code>).
- <code>{0}bc</code>: Broadcast ke semua chat (grup, user, channel).
- <code>{0}stopg</code>: Hentikan semua broadcast yang sedang berjalan.
- <code>{0}autogikes</code>: Auto broadcast dengan delay.

<b>Blacklist:</b>
- <code>{0}addbl</code>: Tambahkan chat/user ke blacklist.
- <code>{0}unbl</code>: Hapus dari blacklist.
- <code>{0}listbl</code>: Lihat daftar blacklist.
- <code>{0}rallbl</code>: Hapus semua blacklist.

<b>Format AutoGikes:</b>
- <code>autogikes on [text] [delay] [limit]</code>
- Contoh: <code>autogikes on Halo! 30 5</code> (kirim 5x dengan jeda 30 detik).
"""

# Variabel Global
gcast_progress = set()
AG = []  # AutoGikes status
chat_cache = {}

# Fungsi Helper untuk mendapatkan chat target
async def get_target_chats(client, target):
    chat_types = {
        "all": [ChatType.PRIVATE, ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL],
        "group": [ChatType.GROUP, ChatType.SUPERGROUP],
        "users": [ChatType.PRIVATE]
    }

    chats = [dialog.chat.id async for dialog in client.get_dialogs() if dialog.chat.type in chat_types.get(target, [])]
    return chats


# Fungsi untuk mengecek dan mengelola blacklist
async def is_blacklisted(chat_id):
    return await is_blacklisted(chat_id)

async def add_to_blacklist(chat_id):
    await add_blacklist(chat_id)

async def remove_from_blacklist(chat_id):
    await remove_blacklist(chat_id)

async def clear_blacklist():
    blacklist_chats = await get_blacklist()
    for chat in blacklist_chats:
        await remove_blacklist(chat["chat_id"])

async def get_blacklist_chats():
    return await get_blacklist()

# Fungsi untuk mengirim broadcast
async def send_broadcast(client, message, target, bcs_label):
    global gcast_progress
    gcast_progress.add(client.me.id)

    # Menggunakan emoji untuk status
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)

    msg = await message.reply(f"<b>{prs} Processing broadcast...</b>")

    # Ambil teks atau pesan reply
    send_content = message.reply_to_message if message.reply_to_message else " ".join(message.command[1:])
    if not send_content:
        gcast_progress.remove(client.me.id)
        return await msg.edit("<b>Silakan balas ke pesan atau berikan teks.</b>")

    # Ambil daftar chat berdasarkan target
    chats = await get_target_chats(client, target)
    done_users, done_groups, failed = 0, 0, 0

    for chat_id in chats:
        if client.me.id not in gcast_progress:
            return await msg.edit("<b>🚫 Broadcast dibatalkan!</b>")

        if await is_blacklisted(chat_id):
            continue  # Lewati chat yang ada dalam blacklist

        try:
            # Jika ada pesan reply/media, gunakan copy
            if message.reply_to_message:
                await message.reply_to_message.copy(chat_id)
            else:
                await client.send_message(chat_id, send_content)

            # Hitung jumlah pesan terkirim
            if target == "users":
                done_users += 1
            else:
                done_groups += 1

        except FloodWait as e:
            wait_time = min(e.value, 60)  # Maksimum tunggu 60 detik
            print(f"[INFO] FloodWait encountered. Waiting {wait_time} seconds.")
            await asyncio.sleep(wait_time)

            # Coba kirim ulang setelah menunggu
            try:
                if message.reply_to_message:
                    await message.reply_to_message.copy(chat_id)
                else:
                    await client.send_message(chat_id, send_content)

                if target == "users":
                    done_users += 1
                else:
                    done_groups += 1

            except Exception:
                failed += 1

        except Exception:
            failed += 1  # Hitung jumlah gagal
            pass

    gcast_progress.remove(client.me.id)
    await msg.delete()  # Hapus pesan status awal

    # Laporan hasil broadcast dengan emoji yang diminta
    report = f"""
{bcs}<emoji id=6037164425356514018>😘</emoji><emoji id=6037583326401794925>😘</emoji><emoji id=6037242439142481737>😘</emoji><emoji id=6037315105694160163>😘</emoji><emoji id=6037431009681609488>😘</emoji><emoji id=6037252029804450164>😘</emoji><emoji id=6034895892350245694>😘</emoji><emoji id=6037220122492408602>😘</emoji><emoji id=6037164425356514018>😘</emoji>

<b>{bcs_label} selesai!</b>
<b>{brhsl} berhasil kirim ke {done_users} user dan {done_groups} group</b>
<b>{ggl} gagal kirim ke {failed} chat</b>
"""
    return await message.reply(report)
@DANTE.UBOT("autogikes")
async def autogikes_handler(client, message):
    args = message.command[1:]
    if not args:
        return await message.reply("Gunakan format: autogikes on/off [text] [user/group] [delay] [limit]")
    
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)
    
    action = args[0].lower()
    if action == "off":
        if client.me.id in AG:
            AG.remove(client.me.id)
            return await message.reply(f"{brhsl} AutoGikes dimatikan! Sebelumnya berhasil mengirim {sent} pesan.")
        else:
            return await message.reply(f"{ggl} AutoGikes tidak sedang berjalan!")
# Helper Functions
def is_blacklisted(chat_id):
    return chat_id in blacklist

def add_to_blacklist(chat_id):
    blacklist.add(chat_id)

def remove_from_blacklist(chat_id):
    blacklist.discard(chat_id)

def clear_blacklist():
    blacklist.clear()

def get_blacklist():
    return list(blacklist)

async def get_target_chats(client, target):
    if target in chat_cache:
        return chat_cache[target]
    
    chat_types = {
        "all": [ChatType.PRIVATE, ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL],
        "group": [ChatType.GROUP, ChatType.SUPERGROUP],
        "users": [ChatType.PRIVATE]
    }
    chat_cache[target] = [dialog.chat.id async for dialog in client.get_dialogs() if dialog.chat.type in chat_types.get(target, [])]
    return chat_cache[target]

async def send_broadcast(client, message, target, bcs_label):
    global gcast_progress
    gcast_progress.add(client.me.id)
    
    # Menggunakan emoji untuk status
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)

    msg = await message.reply(f"<b>{prs} Processing broadcast...</b>")

    # Ambil teks atau pesan reply
    send_content = message.reply_to_message if message.reply_to_message else " ".join(message.command[1:])
    if not send_content:
        gcast_progress.remove(client.me.id)
        return await msg.edit("<b>Silakan balas ke pesan atau berikan teks.</b>")
    
    # Ambil daftar chat berdasarkan target
    chats = await get_target_chats(client, target)
    done_users, done_groups, failed = 0, 0, 0
    
    for chat_id in chats:
        if client.me.id not in gcast_progress:
            return await msg.edit("<b>🚫 Broadcast dibatalkan!</b>")

        if chat_id in blacklist:
            continue  # Lewati chat yang ada dalam blacklist

        try:
            # Jika ada pesan reply/media, gunakan copy
            if message.reply_to_message:
                await message.reply_to_message.copy(chat_id)
            else:
                await client.send_message(chat_id, send_content)
            
            # Hitung jumlah pesan terkirim
            if target == "users":
                done_users += 1
            else:
                done_groups += 1

        except FloodWait as e:
            wait_time = min(e.value, 60)  # Maksimum tunggu 60 detik
            print(f"[INFO] FloodWait encountered. Waiting {wait_time} seconds.")
            await asyncio.sleep(wait_time)

            # Coba kirim ulang setelah menunggu
            try:
                if message.reply_to_message:
                    await message.reply_to_message.copy(chat_id)
                else:
                    await client.send_message(chat_id, send_content)

                if target == "users":
                    done_users += 1
                else:
                    done_groups += 1

            except Exception:
                failed += 1

        except Exception:
            failed += 1  # Hitung jumlah gagal
            pass
    
    gcast_progress.remove(client.me.id)
    await msg.delete()  # Hapus pesan status awal

    # Laporan hasil broadcast dengan emoji yang diminta
    report = f"""
{bcs}<emoji id=6037164425356514018>😘</emoji><emoji id=6037583326401794925>😘</emoji><emoji id=6037242439142481737>😘</emoji><emoji id=6037315105694160163>😘</emoji><emoji id=6037431009681609488>😘</emoji><emoji id=6037252029804450164>😘</emoji><emoji id=6034895892350245694>😘</emoji><emoji id=6037220122492408602>😘</emoji><emoji id=6037164425356514018>😘</emoji>

<b>{bcs_label} selesai!</b>
<b>{brhsl} berhasil kirim ke {done_users} user dan {done_groups} group</b>
<b>{ggl} gagal kirim ke {failed} chat</b>
"""
    return await message.reply(report)

# Commands untuk broadcast
@DANTE.UBOT("gcast")
async def gcast_handler(client, message):
    """Mengirim broadcast ke semua grup"""
    await send_broadcast(client, message, "group", "📢 GCAST")

@DANTE.UBOT("ucast")
async def ucast_handler(client, message):
    """Mengirim broadcast ke semua user yang terdaftar"""
    await send_broadcast(client, message, "users", "📢 UCAST")

@DANTE.UBOT("bc")
async def bc_handler(client, message):
    """Mengirim broadcast ke semua chat (user, grup, dan channel)"""
    await send_broadcast(client, message, "all", "📢 Broadcast")


# Command untuk menghentikan broadcast
@DANTE.UBOT("stopg")
async def stopg_handler(client, message):
    """Menghentikan semua broadcast yang sedang berjalan"""
    global gcast_progress

    if client.me.id in gcast_progress:
        gcast_progress.remove(client.me.id)
        await message.reply("<b>🚫 Broadcast dihentikan!</b>")
    else:
        await message.reply("<b>⚠️ Tidak ada broadcast yang berjalan.</b>")


# Fungsi Helper untuk mengecek dan mengelola AutoGikes
async def set_autogikes_settings(user_id, text, target, delay, limit):
    await set_autogikes(user_id, text, target, delay, limit)

async def get_autogikes_settings(user_id):
    return await get_autogikes(user_id)

async def remove_autogikes_settings(user_id):
    await remove_autogikes(user_id)

# Perintah untuk AutoGikes
@DANTE.UBOT("autogikes")
async def autogikes_handler(client, message):
    """
    Mengaktifkan atau menonaktifkan AutoGikes.
    Format:
    - autogikes on [text] [user/group] [delay] [limit]
    - autogikes off
    """
    args = message.command[1:]

    if not args:
        return await message.reply("Gunakan format: autogikes on/off [text] [user/group] [delay] [limit]")

    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)

    action = args[0].lower()
    if action == "on":
        if client.me.id in AG:
            return await message.reply("⚠️ AutoGikes sudah berjalan!")

        try:
            text = args[1]
            target = args[2].lower()
            if target not in ["user", "group"]:
                return await message.reply("⚠️ Target harus 'user' atau 'group'")
            delay = int(args[3])
            limit = int(args[4])
        except (IndexError, ValueError):
            return await message.reply("⚠️ Format salah! Gunakan: autogikes on [text] [user/group] [delay] [limit]")

        AG.append(client.me.id)
        await set_autogikes(client.me.id, text, target, delay, limit)  # Simpan pengaturan AutoGikes ke database
        
        count, sent_users, sent_groups, failed = 0, 0, 0, 0

        while client.me.id in AG and count < limit:
            chats = await get_target_chats(client, target)
            for chat_id in chats:
                if await is_blacklisted(chat_id):
                    continue
                try:
                    await client.send_message(chat_id, text)
                    if target == "users":
                        sent_users += 1
                    else:
                        sent_groups += 1
                except Exception:
                    failed += 1
                await asyncio.sleep(delay)
            count += 1

        AG.remove(client.me.id)
        await remove_autogikes(client.me.id)  # Hapus pengaturan AutoGikes dari database setelah selesai

        # Laporan hasil AutoGikes dengan emoji
        report = f"""
{bcs}<emoji id=6037164425356514018>😘</emoji><emoji id=6037583326401794925>😘</emoji><emoji id=6037242439142481737>😘</emoji><emoji id=6037315105694160163>😘</emoji><emoji id=6037431009681609488>😘</emoji><emoji id=6037252029804450164>😘</emoji><emoji id=6034895892350245694>😘</emoji><emoji id=6037220122492408602>😘</emoji><emoji id=6037164425356514018>😘</emoji>

<b>AutoGikes selesai!</b>

✅ <b>{brhsl}Berhasil terkirim ke:</b>
- 👤 {sent_users} User 
- 💬 {sent_groups} Grup

❌ <b>{ggl}Gagal terkirim ke:</b>
- {failed} Chat

<b>Total putaran: {count} kali</b>
"""
        return await message.reply(report)

    elif action == "off":
        if client.me.id in AG:
            AG.remove(client.me.id)
            await remove_autogikes(client.me.id)  # Hapus pengaturan AutoGikes dari database saat dimatikan
            return await message.reply(f"{brhsl} ✅ AutoGikes dimatikan!")
        else:
            return await message.reply(f"{ggl} ⚠️ AutoGikes tidak sedang berjalan!")


# Commands untuk mengelola blacklist
@DANTE.UBOT("addbl")
async def add_blacklist_command(client, message):
    """Menambahkan chat ke blacklist"""
    chat_id = message.chat.id if not message.reply_to_message else message.reply_to_message.chat.id
    if await is_blacklisted(chat_id):
        return await message.reply("<b>Chat/User sudah dalam blacklist.</b>")
    await add_blacklist(chat_id)
    await message.reply("<b>Berhasil ditambahkan ke blacklist.</b>")

@DANTE.UBOT("unbl")
async def remove_blacklist_command(client, message):
    """Menghapus chat dari blacklist"""
    chat_id = message.chat.id if not message.reply_to_message else message.reply_to_message.chat.id
    if not await is_blacklisted(chat_id):
        return await message.reply("<b>Chat/User tidak ada dalam blacklist.</b>")
    await remove_blacklist(chat_id)
    await message.reply("<b>Berhasil dihapus dari blacklist.</b>")

@DANTE.UBOT("listbl")
async def list_blacklist_command(client, message):
    """Menampilkan daftar blacklist"""
    bl_list = await get_blacklist()
    if not bl_list:
        return await message.reply("<b>Blacklist kosong.</b>")
    text = "<b>Daftar Blacklist:</b>\n" + "\n".join(f"<b>- {chat['chat_id']}</b>" for chat in bl_list)
    await message.reply(text)

@DANTE.UBOT("rallbl")
async def clear_blacklist_command(client, message):
    """Menghapus semua data blacklist"""
    await clear_blacklist()
    await message.reply("<b>Semua blacklist telah dihapus.</b>")

@DANTE.INLINE("^get_send_")
async def send_inline(client, inline_query):
    """
    Menangani inline query untuk mengirim pesan atau media.
    Format:
    - Jika reply ke gambar: Mengunggah ke Telegraph & mengirimkan sebagai inline query
    - Jika reply ke teks: Mengirim teks sebagai inline query
    """
    try:
        _id = int(inline_query.query.split()[1])
        message = [obj for obj in get_objects() if id(obj) == _id][0]

        if message.reply_to_message.photo:
            # Mengunggah gambar ke Telegraph
            downloaded_media = await message.reply_to_message.download()
            photo_tg = upload_file(downloaded_media)
            caption = message.reply_to_message.caption or ""
            result = [
                InlineQueryResultPhoto(
                    photo_url=f"https://telegra.ph/{photo_tg[0]}",
                    title="Broadcast Media",
                    caption=caption
                ),
            ]
            os.remove(downloaded_media)
        else:
            # Mengirim pesan teks
            result = [
                InlineQueryResultArticle(
                    title="Broadcast Text",
                    input_message_content=InputTextMessageContent(message.reply_to_message.text),
                )
            ]

        await client.answer_inline_query(inline_query.id, cache_time=0, results=result)
    except Exception as e:
        print(f"Error handling inline query: {e}")

