import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from DanteUserbot import *
from DanteUserbot.core.database.logs import (
    enable_logging, disable_logging, is_logging_enabled,
    add_nolog_user, remove_nolog_user, get_nolog_users,
    set_log_option, get_log_option
)

__MODULE__ = "ʟᴏɢs"
__HELP__ = f"""<blockquote><b>
<b>『 Bantuan untuk Logs 』</b>

  <b>• Perintah:</b> <code>{PREFIX[0]}log1</code> [on/off]
  <b>• Penjelasan:</b> Mengaktifkan atau menonaktifkan logging dikirim ke pesan pribadi.

  <b>• Perintah:</b> <code>{PREFIX[0]}logop</code> [on/off group/chat]
  <b>• Penjelasan:</b> Memilih log yang diterima.
    - <code>on group</code> → Hanya log dari grup.
    - <code>on chat</code> → Hanya log pesan pribadi.
    - <code>off</code> → Semua log masuk.

  <b>• Perintah:</b> <code>{PREFIX[0]}nolog</code> [username]
  <b>• Penjelasan:</b> Mengabaikan pesan dari pengguna tertentu.
</b></blockquote>
"""

LOGS = logging.getLogger(__name__)

@DANTE.UBOT("log1")  # Correct usage with a valid command string
async def log_toggle(client, message):
    """Mengaktifkan atau menonaktifkan logging untuk pengguna tertentu."""
    user_id = message.from_user.id
    command = message.text.split()
    
    if len(command) < 2:
        return await message.reply_text("Gunakan `/log1 on` atau `/log1 off`.")

    action = command[1].lower()
    if action == "on":
        await enable_logging(user_id)
        await message.reply_text("✅ Logging telah diaktifkan.")
    elif action == "off":
        await disable_logging(user_id)
        await message.reply_text("❌ Logging telah dinonaktifkan.")
    else:
        await message.reply_text("Format salah. Gunakan `/log1 on` atau `/log1 off`.")

@DANTE.UBOT("logop")  # Correct usage with a valid command string
async def set_logging_option(client, message):
    """Mengatur opsi log: 'all', 'group', atau 'chat'."""
    user_id = message.from_user.id
    command = message.text.split()

    if len(command) < 3:
        return await message.reply_text("Gunakan `/logop on group/chat` atau `/logop off`.")

    action, option = command[1].lower(), command[2].lower()

    if action == "on" and option in ["group", "chat"]:
        await set_log_option(user_id, option)
        await message.reply_text(f"✅ Logging hanya untuk **{option}** diaktifkan.")
    elif action == "off":
        await set_log_option(user_id, "all")
        await message.reply_text("✅ Semua log diaktifkan kembali.")
    else:
        await message.reply_text("❌ Format salah. Gunakan `/logop on group/chat` atau `/logop off`.")

@DANTE.UBOT("nolog")  # Correct usage with a valid command string
async def ignore_user(client, message):
    """Menambahkan pengguna ke daftar yang diabaikan dalam logging."""
    owner_id = message.from_user.id
    command = message.text.split()
    if len(command) < 2:
        return await message.reply_text("Gunakan `/nolog @username`.")
    
    try:
        user = await client.get_users(command[1])
        await add_nolog_user(owner_id, user.id)
        await message.reply_text(f"🔕 Pesan dari {user.mention} tidak akan dicatat lagi.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@DANTE.UBOT("log_private_messages", filter=filters.private)  # Use a valid command string and filter
async def log_private_messages(client, message):
    """Merekam pesan pribadi dan mengirimkan ke chat pengguna bot."""
    user_id = message.from_user.id
    log_option = await get_log_option(user_id)
    
    if await is_logging_enabled(user_id) and log_option in ["all", "chat"]:
        ignored_users = await get_nolog_users(user_id)
        if message.from_user.id in ignored_users:
            return  # Abaikan pengguna yang masuk daftar `nolog`

        try:
            if message.text:
                text = (
                    f"📨 **Pesan Pribadi dari [{message.from_user.first_name}](tg://user?id={message.from_user.id})**\n\n"
                    f"**💬 Pesan:**\n{message.text}"
                )
                await client.send_message(user_id, text)
            elif message.media:
                media_caption = message.caption or "📂 **Media tanpa keterangan**"
                await message.copy(user_id, caption=f"📨 **Pesan Pribadi dari {message.from_user.first_name}**\n\n{media_caption}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await log_private_messages(client, message)

@DANTE.UBOT("log_mentions", filter=filters.mentioned)  # Use a valid command string and filter
async def log_mentions(client, message):
    """Merekam pesan mention di grup dan mengirimkan ke chat pengguna bot."""
    user_id = message.from_user.id
    log_option = await get_log_option(user_id)

    if await is_logging_enabled(user_id) and log_option in ["all", "group"]:
        ignored_users = await get_nolog_users(user_id)
        if message.from_user.id in ignored_users:
            return  # Abaikan pengguna yang masuk daftar `nolog`

        try:
            user = message.from_user.mention
            message_link = f"https://t.me/c/{message.chat.id}/{message.message_id}"
            text = (
                f"📨 **#TAGGED_MESSAGE**\n"
                f"• [{user}](tg://user?id={message.from_user.id}) menyebutkan Anda di {message.chat.title}:\n"
                f"{message.text or '📂 Media'}\n"
                f"[🔗 Lihat Pesan]({message_link})"
            )
            await client.send_message(user_id, text)
            if message.media:
                await message.copy(user_id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await log_mentions(client, message)
