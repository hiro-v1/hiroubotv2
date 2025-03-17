from pyrogram import Client, filters
import asyncio
import time
from DanteUserbot import *
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait, RPCError
from pyrogram.types import Message, ChatPermissions

@DANTE.UBOT("delallc")
async def deleteall(client: Client, message: Message):
    """Menghapus semua pesan dari pengguna yang di-reply."""
    if not message.reply_to_message:
        return await message.edit("__Balas pesan pengguna untuk menghapus semua pesan.__")

    dante = await message.edit("__Menghapus semua pesan pengguna ini...__")
    user_id = message.reply_to_message.from_user.id

    try:
        await client.delete_user_history(message.chat.id, user_id)
        await dante.edit("__Semua pesan dari pengguna ini telah dihapus.__")
    except Exception as e:
        await dante.edit(f"❌ **Gagal menghapus pesan:** {e}")

@DANTE.UBOT("unblockall")
async def unblockall(client: Client, message: Message):
    """Membuka blokir semua pengguna di grup/channel."""
    chat_id = message.chat.id
    chat_name = message.chat.title

    if len(message.command) > 1:
        try:
            chat = await client.get_chat(message.command[1])
            chat_id = chat.id
            chat_name = chat.title
        except RPCError as e:
            return await message.edit(f"❌ **ID Grup tidak valid.**\n\n`{e}`")

    dante = await message.edit(f"🔄 **Membuka blokir semua pengguna di** `{chat_name}`...")

    total = 0
    success = 0
    async for user in client.get_chat_members(chat_id, filter=ChatMembersFilter.BANNED):
        total += 1
        try:
            await client.unblock_user(user.user.id)
            success += 1
            await asyncio.sleep(1)  # Delay untuk menghindari rate limit
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except Exception:
            pass  # Abaikan error lainnya

    await dante.edit(
        f"✅ **Unblock All Selesai!**\n\n"
        f"🔹 **Total pengguna terblokir:** {total}\n"
        f"✅ **Berhasil di-unblock:** {success}\n"
        f"❌ **Gagal di-unblock:** {total - success}"
    )

    # Logging tambahan (jika dibutuhkan)
    await client.send_message(
        OWNER_ID, 
        f"📢 **Laporan UnblockAll**\n\n"
        f"🔹 **Grup:** {chat_name}\n"
        f"🔹 **Total:** {total}\n"
        f"✅ **Unblocked:** {success}\n"
        f"❌ **Failed:** {total - success}\n\n"
        f"🔹 **Dijalankan oleh:** {client.me.mention}"
    )
