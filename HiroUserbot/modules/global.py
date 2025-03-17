from HiroUserbot import *

__MODULE__ = "ɢʙᴀɴ"
__HELP__ = f"""<blockquote><b>
<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ɢʟᴏʙᴀʟ 』</b>

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}gban</code> [ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ʙᴀɴɴᴇᴅ ᴜsᴇʀ ᴅᴀʀɪ sᴇᴍᴜᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ 

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}ungban</code> [ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴜɴʙᴀɴɴᴇᴅ ᴜsᴇʀ ᴅᴀʀɪ sᴇᴍᴜᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{PREFIX[0]}listgban</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴅᴀꜰᴛᴀʀ ᴘᴇɴɢɢᴜɴᴀ ɢʙᴀɴ.

</b></blockquote>"""
import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from pyrogram.errors import *
from pyrogram.types import *
from HiroUserbot.core.function.emoji import emoji

BANNED_USERS = filters.user()            


async def global_banned(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id = await extract_user(message)
    Tm = await eor(message, f"{prs}<code>ᴍᴇᴍᴘʀᴏꜱᴇꜱ....</code>")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await Tm.edit(
            f"{ggl}<code>gban</code> [uꜱer_id/uꜱername/reply to uꜱer]"
        )
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
    try:
        user = await client.get_users(user_id)
    except PeerIdInvalid:
        await Tm.edit(f"{ggl}ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴜꜱᴇʀ ᴛᴇʀꜱᴇʙᴜᴛ.")
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
                    f"{ggl}<b>ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ɢʙᴀɴ ᴅɪᴀ ᴋᴀʀᴇɴᴀ ᴅɪᴀ ᴘᴇᴍʙᴜᴀᴛ ꜱᴀʏᴀ</b>."
                )
            elif prik in prok:
                return await Tm.edit(
                    f"{ggl}<b>ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ɢʙᴀɴ ᴅɪᴀ, ᴋᴀʀɴᴀ ᴅɪᴀ ᴀᴅᴀʟᴀʜ ᴀᴅᴍɪɴ ᴜꜱᴇʀʙᴏᴛ ᴀɴᴅᴀ</b>."
                )
            elif udah:
                return await Tm.edit(
                    f"{sks}<b>ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ ꜱᴜᴅᴀʜ ᴅɪ ɢʙᴀɴ</b>"
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
<b>{ttl}ɢʟᴏʙᴀʟ ʙᴀɴɴᴇᴅ</b>

<b>{sks}ʙᴇʀʜᴀꜱɪʟ ʙᴀɴɴᴇᴅ: {iso} ᴄʜᴀᴛ</b>
<b>{ggl}ɢᴀɢᴀʟ ʙᴀɴɴᴇᴅ: {gagal} ᴄʜᴀᴛ</b>
<b>uꜱer: <a href='tg://user?id={prik}'>{user.first_name}</a></b>
"""
    )

async def cung_ban(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id = await extract_user(message)
    if message.from_user.id != client.me.id:
        Tm = await eor(f"{prs}<code>ᴍᴇᴍᴘʀᴏꜱᴇꜱ.....</code>")
    else:
        Tm = await eor(message, f"{prs}<code>ᴍᴇᴍᴘʀᴏꜱᴇꜱ....</code>")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await Tm.edit(
            f"{ggl}<code>ungban</code> [uꜱer_id/uꜱername/reply to uꜱer]"
        )
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
    try:
        user = await client.get_users(user_id)
    except PeerIdInvalid:
        await Tm.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴜꜱᴇʀ ᴛᴇʀꜱᴇʙᴜᴛ</b>")
        return
    iso = 0
    gagal = 0
    prik = user.id
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
            if prik in BANNED_USERS:
                BANNED_USERS.remove(prik) 
            try:
                await remove_banned_user(gua, prik)
                await client.unban_chat_member(chat, prik)
                iso = iso + 1
                await asyncio.sleep(0.1)
            except BaseException:
                gagal = gagal + 1
                await asyncio.sleep(0.1)

    return await Tm.edit(
        f"""
<b>{ttl}ɢʟᴏʙᴀʟ ʙᴀɴɴᴇᴅ</b>

<b>{sks}ʙᴇʀʜᴀꜱɪʟ ʙᴀɴɴᴇᴅ: {iso} ᴄʜᴀᴛ</b>
<b>{ggl}ɢᴀɢᴀʟ ʙᴀɴɴᴇᴅ: {gagal} ᴄʜᴀᴛ</b>
<b>uꜱer: <a href='tg://user?id={prik}'>{user.first_name}</a></b>
"""
    )


async def gbanlist(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    gua = client.me.id
    total = await get_banned_count(gua)
    if total == 0:
        return await message.edit(f"{ggl}<b>ʙᴇʟᴜᴍ ᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴅɪɢʙᴀɴ.</b>")
    nyet = await message.edit(f"{prs}<b>ᴍᴇᴍᴘʀᴏꜱᴇꜱ...</b>")
    msg = "ᴛᴏᴛᴀʟ ɢʙᴀɴɴᴇᴅ:\n\n"
    tl = 0
    org = await get_banned_users(gua)
    for i in org:
        tl += 1
        try:
            user = await client.get_users(i)
            user = (
                user.first_name if not user.mention else user.mention
            )
            msg += f"{tl}• {user}\n"
        except Exception:
            msg += f"{tl}• {i}\n"
            continue
    if tl == 0:
        return await nyet.edit(f"{ggl}<b>ʙᴇʟᴜᴍ ᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴅɪɢʙᴀɴ.</b>")
    else:
        return await nyet.edit(msg)


@HIRO.UBOT("gban")
#@ubot.on_message(filters.user(DEVS) & filters.command("cgban", "") & ~filters.me)
async def _(client, message):
    await global_banned(client, message)


@HIRO.UBOT("ungban")
async def _(client, message):
    await cung_ban(client, message)


@HIRO.UBOT("listgban")
async def _(client, message):
    await gbanlist(client, message)
