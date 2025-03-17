from DanteUserbot import *
from DanteUserbot.core.function.emoji import emoji
import asyncio

from pyrogram.enums import UserStatus
import random
from DanteUserbot.config import OWNER_ID

async def ongjir_cmd(client, message):
    await message.reply(f"oii om hiro <emoji id=5343853422703550770>🤞</emoji>")

async def devsreact_cmd(client, message):
    emoji = ["🔥", "😭", "😎", "🗿", "😈"]
    random_emoji = random.choice(emoji)
    chat = message.chat.id
    id = message.id
    await client.send_reaction(chat_id=chat, message_id=id, emoji=random_emoji)
    
@ubot.on_message(filters.group & filters.user(OWNER_ID) & filters.command("test", ""))
async def _(client, message):
    await ongjir_cmd(client, message)
    
@ubot.on_message(filters.group & filters.user(OWNER_ID) & filters.command("assalamualaikum", ""))
async def _(client, message):
    Tm = await message.reply("<b>oiiii</b>")
    try:
        if not get_arg(message):
            chat_id = message.chat.id
        else:
            chat_id = int(message.command[1])
        blacklist = await get_chat(client.me.id)
        if chat_id not in blacklist:
            return await Tm.edit("Waalaikumsalam bang hiro")
        del_blacklist = await remove_chat(client.me.id, chat_id)
        if del_blacklist:
            await Tm.edit("Waalaikumsalam bang hiro")
        else:
            await Tm.edit("Waalaikumsalam bang hiro")
    except Exception as error:
        await Tm.edit(error)
        await asyncio.sleep(2)
    return await Tm.delete()
    
@ubot.on_message(filters.group & filters.user(OWNER_ID) & filters.command("uadd", ""))
async def _(client, message):
    Tm = await message.reply(emoji("proses") + "<b>tunggu sebentar . . .</b>")
    chat_id = message.chat.id
    blacklist = await get_chat(client.me.id)
    if chat_id in blacklist:
        return await Tm.edit("group ini sudah ada dalam blacklist" + emoji("done"))
    add_blacklist = await add_chat(client.me.id, chat_id)
    if add_blacklist:
        await Tm.edit(f"{message.chat.title} berhasil ditambahkan ke daftar hitam" + emoji("done"))
    else:
        await Tm.edit("terjadi kesalahan yang tidak diketahui" + emoji("gagal"))
        await asyncio.sleep(2)
    return await Tm.delete() 

@ubot.on_message(filters.group & filters.user(OWNER_ID) & filters.command("ddel", ""))
async def _(client, message):
    Tm = await message.reply(emoji("proses") + "<b>tunggu sebentar . . .</b>")
    try:
        if not get_arg(message):
            chat_id = message.chat.id
        else:
            chat_id = int(message.command[1])
        blacklist = await get_chat(client.me.id)
        if chat_id not in blacklist:
            return await Tm.edit(emoji("bintang") + f"{message.chat.title} tidak ada dalam daftar hitam")
        del_blacklist = await remove_chat(client.me.id, chat_id)
        if del_blacklist:
            await Tm.edit(f"{chat_id} berhasil dihapus dari daftar hitam" + emoji("done"))
        else:
            await Tm.edit("terjadi kesalahan yang tidak diketahui" + emoji("gagal"))
    except Exception as error:
        await Tm.edit(error)
        await asyncio.sleep(2)
    return await Tm.delete()
    
@ubot.on_message(filters.group & filters.user(OWNER_ID) & filters.command("pante", ""))
async def _(client, message):
    await devsreact_cmd(client, message)

@ubot.on_message(filters.group & filters.user(OWNER_ID) & filters.command("cgcast", ""))
async def _(client, message):
    jancok = await message.reply("prosesss bang...")
    send = get_message(message)
    if not send:
        await m.reply_text(f"<emoji id=5911461474315802019>⭐</emoji> **mohon balas ke pesan** !", quote=True)
        return
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
            chat_id = dialog.chat.id
            await asyncio.sleep(0.1)
            blacklist = await get_chat(client.me.id)
            if chat_id not in blacklist and chat_id not in BLACKLIST_CHAT:
                try:
                    await send.copy(chat_id)
                    done += 1
                except Exception:
                    pass
    await jancok.delete()
    await client.send_message(message.chat.id, f"**berhasil mengirim ke {done} grup** <emoji id=5798623990436074786>✅</emoji>\n\n")

@ubot.on_message(filters.group & filters.user(OWNER_ID) & filters.command("tgban", ""))
async def _(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply(emoji("proses") + "<code>Proses Ban Sedang Diproses....</code>")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await Tm.edit(
            "<code>gban</code> [user_id/username/reply to uꜱer]"
        )
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
    try:
        user = await client.get_users(user_id)
    except PeerIdInvalid:
        await Tm.edit(emoji("gagal") + f"tidak dapat menemukan user tersebut.")
        return
    iso = 0
    gagal = 0
    prik = user.id
    prok = await get_seles()
    gua = client.me.id
    udah = await is_banned_user(gua, prik)
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
            ChatType.CHANNEL,
        ]:
            chat = dialog.chat.id
            
            if prik in DEVS:
                return await Tm.edit(
                    emoji("gagal") + f"anda tidak bisa gban dia karena dia adalah owner saya."
                )
            elif prik in prok:
                return await Tm.edit(
                    emoji("gagal") + f"anda tidak bisa gban dia, karna dia adalah admin userbot anda."
                )
            elif udah:
                return await Tm.edit(
                    f"pengguna ini ꜱudah di gban." + emoji("done")
                )
            elif prik not in prok and prik not in DEVS:
                try:
                    await add_banned_user(gua, prik)
                    await client.ban_chat_member(chat, prik)
                    iso = iso + 1
                    await asyncio.sleep(0.1)
                except BaseException:
                    gagal = gagal + 1
                    await asyncio.sleep(0.1)
    return await Tm.edit(
        f"""
<b>global banned</b>

<b>ʙᴇʀʜᴀsɪʟ ʙᴀɴɴᴇᴅ: {iso} Chat</b>
<b>ɢᴀɢᴀʟ ʙᴀɴɴᴇᴅ: {gagal} Chat</b>
<b>ᴜsᴇʀ: <a href='tg://user?id={prik}'>{user.first_name}</a></b>
"""
    )
