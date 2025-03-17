from DanteUserbot import *
from DanteUserbot.core.database.saved import get_chat
from pyrogram import Client, enums, filters
from pyrogram.types import Message
import asyncio
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from DanteUserbot.core.function.emoji import emoji

__MODULE__ = "Gabung"
__HELP__ = f"""<blockquote><b>
<b>『 Bantuan Join & Leave 』</b>

  <b>• Perintah:</b> <code>{PREFIX[0]}kickme</code>
  <b>• Penjelasan:</b> Keluar dari grup saat ini.

  <b>• Perintah:</b> <code>{PREFIX[0]}join</code> [username/id]
  <b>• Penjelasan:</b> Bergabung ke grup/channel dengan username atau ID.

  <b>• Perintah:</b> <code>{PREFIX[0]}leave</code> [username/id]
  <b>• Penjelasan:</b> Keluar dari grup dengan username atau ID.

  <b>• Perintah:</b> <code>{PREFIX[0]}leaveallgc</code>
  <b>• Penjelasan:</b> Keluar dari semua grup yang bukan admin/owner.

  <b>• Perintah:</b> <code>{PREFIX[0]}leaveallmute</code>
  <b>• Penjelasan:</b> Keluar dari semua grup yang membatasi Anda.

  <b>• Perintah:</b> <code>{PREFIX[0]}leaveallch</code>
  <b>• Penjelasan:</b> Keluar dari semua channel yang bukan admin/owner.
</b></blockquote>"""

# ✅ Perintah untuk keluar dari grup secara manual
@DANTE.UBOT("kickme|leave")
async def leave(client: Client, message: Message):
    ggl, sks, prs = await EMO.GAGAL(client), await EMO.BERHASIL(client), await EMO.PROSES(client)
    target_chat = message.command[1] if len(message.command) > 1 else message.chat.id

    if message.chat.id in BLACKLIST_CHAT:
        return await message.reply(f"{ggl} Perintah ini dilarang digunakan di grup ini.")

    try:
        await message.reply(f"{prs} Sedang memproses keluar...")
        await client.leave_chat(target_chat)
        await message.reply(f"{sks} Berhasil keluar dari grup ini. Bye!")
    except Exception as ex:
        await message.reply(f"{ggl} ERROR:\n\n{str(ex)}")

# ✅ Perintah untuk join ke grup
@DANTE.UBOT("join")
async def join(client: Client, message: Message):
    ggl, sks, prs = await EMO.GAGAL(client), await EMO.BERHASIL(client), await EMO.PROSES(client)
    target_chat = message.command[1] if len(message.command) > 1 else None

    if not target_chat:
        return await message.reply(f"{ggl} Harap berikan username atau ID grup untuk join.")

    try:
        await message.reply(f"{prs} Sedang bergabung ke `{target_chat}`...")
        await client.join_chat(target_chat)
        await message.reply(f"{sks} Berhasil bergabung ke `{target_chat}`.")
    except Exception as ex:
        await message.reply(f"{ggl} ERROR:\n\n{str(ex)}")

# ✅ Perintah untuk keluar dari semua grup yang bukan admin/owner
@DANTE.UBOT("leaveallgc")
async def leave_all_groups(client, message):
    ggl, sks, prs = await EMO.GAGAL(client), await EMO.BERHASIL(client), await EMO.PROSES(client)
    left_count = 0

    await message.reply(f"{prs} Sedang memproses keluar dari semua grup...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
            try:
                member = await client.get_chat_member(dialog.chat.id, "me")
                if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                    await client.leave_chat(dialog.chat.id)
                    left_count += 1
                    await asyncio.sleep(0.1)  # Untuk menghindari rate limit
            except Exception:
                pass

    await message.reply(f"{sks} Berhasil keluar dari {left_count} grup yang bukan admin/owner.")

# ✅ Perintah untuk keluar dari semua grup yang membatasi bot
@DANTE.UBOT("leaveallmute")
async def leave_muted_groups(client, message):
    ggl, sks, prs = await EMO.GAGAL(client), await EMO.BERHASIL(client), await EMO.PROSES(client)
    left_count = 0

    await message.reply(f"{prs} Sedang memproses keluar dari semua grup yang membatasi Anda...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
            try:
                member = await client.get_chat_member(dialog.chat.id, "me")
                if member.status == ChatMemberStatus.RESTRICTED:
                    await client.leave_chat(dialog.chat.id)
                    left_count += 1
                    await asyncio.sleep(0.1)
            except Exception:
                pass

    await message.reply(f"{sks} Berhasil keluar dari {left_count} grup yang membatasi Anda.")

# ✅ Perintah untuk keluar dari semua channel yang bukan admin/owner
@DANTE.UBOT("leaveallch")
async def leave_all_channels(client: Client, message: Message):
    ggl, sks, prs = await EMO.GAGAL(client), await EMO.BERHASIL(client), await EMO.PROSES(client)
    left_count = 0

    await message.reply(f"{prs} Sedang memproses keluar dari semua channel...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.CHANNEL:
            try:
                member = await client.get_chat_member(dialog.chat.id, "me")
                if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                    await client.leave_chat(dialog.chat.id)
                    left_count += 1
                    await asyncio.sleep(0.1)
            except Exception:
                pass

    await message.reply(f"{sks} Berhasil keluar dari {left_count} channel yang bukan admin/owner.")
