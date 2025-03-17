__MODULE__ = "ᴀᴅᴍɪɴ"
__HELP__ = """
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴀᴅᴍɪɴ--**
<blockquote><b>
  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}kick</code> [ᴜꜱᴇʀ_ɪᴅ/ᴜꜱᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ ᴜꜱᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴᴇɴᴅᴀɴɢ ᴀɴɢɢᴏᴛᴀ ᴅᴀʀɪ ɢʀᴜᴘ 

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}ban</code> [ᴜꜱᴇʀ_ɪᴅ/ᴜꜱᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ ᴜꜱᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙʟᴏᴋɪʀ ᴀɴɢɢᴏᴛᴀ ᴅᴀʀɪ ɢʀᴜᴘ 

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}mute</code> [ᴜꜱᴇʀ_ɪᴅ/ᴜꜱᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ ᴜꜱᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙɪꜱᴜᴋᴀɴ ᴀɴɢɢᴏᴛᴀ ᴅᴀʀɪ ɢʀᴜᴘ 

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}unmute</code> [ᴜꜱᴇʀ_ɪᴅ/ᴜꜱᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ ᴜꜱᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇʟᴇᴘᴀꜱ ᴘᴇᴍʙʟᴏᴋɪʀᴀɴ ᴀɴɢɢᴏᴛᴀ ᴅᴀʀɪ ɢʀᴜᴘ 

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}unban</code> [ᴜꜱᴇʀ_ɪᴅ/ᴜꜱᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ ᴜꜱᴇʀ]
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇʟᴇᴘᴀꜱ ᴘᴇᴍʙɪꜱᴜᴀɴ ᴀɴɢɢᴏᴛᴀ ᴅᴀʀɪ ɢʀᴜᴘ

  <b>• ᴄᴏᴍᴍᴀɴᴅ:</b> <code>{0}getlink</code>
  <b>• ᴇxᴘʟᴀɴᴀᴛɪᴏɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴍʙɪʟ ʟɪɴᴋ ᴅɪ ɢʀᴜᴘ ᴛᴇʀꜱᴇʙᴜᴛ
 </b></blockquote> """

import asyncio

from asyncio import sleep

from pyrogram import Client, filters
from importlib import import_module
from DanteUserbot.modules import loadModule
from DanteUserbot.core.helpers.misc import *
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from DanteUserbot import *

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@DANTE.UBOT("ban|dban")
async def member_ban(client: Client, message: Message):
    bsl = await EMO.BERHASIL(client)
    ex = await EMO.GAGAL(client)
    meti = await EMO.MENTION(client)
    prs = await EMO.PROSES(client)
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    ky = await eor(message, f"{prs}<b>ᴘʀᴏᴄᴇssɪɴɢ</b>...")
    if not user_id:
        return await ky.edit(f"{ex}ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ.")
    if user_id == client.me.id:
        return await ky.edit(f"{ex}ᴛɪᴅᴀᴋ ʙɪsᴀ ʙᴀɴɴᴇᴅ ᴅɪʀɪ sᴇɴᴅɪʀɪ.")
    if user_id == OWNER_ID:
        return await ky.edit(f"{ex}ᴛɪᴅᴀᴋ ʙɪsᴀ ʙᴀɴɴᴇᴅ Dᴇᴠs!")
    if user_id in (await list_admins(message)):
        return await ky.edit(f"{ex}ᴛɪᴅᴀᴋ ʙɪsᴀ ʙᴀɴɴᴇᴅ ᴀᴅᴍɪɴ.")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "anon"
        )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    msg = f"{bsl}<b>ʙᴀɴɴᴇᴅ ᴜsᴇʀ:</b> {mention}\n{meti}<b>ʙᴀɴɴᴇᴅ ʙʏ:</b> {message.from_user.mention}\n"
    if reason:
        msg += f"{prs}<b>ᴀʟᴀsᴀɴ:</b> {reason}"
    try:
        await message.chat.ban_member(user_id)
        await ky.edit(msg)
        await ky.delete() 
    except ChatAdminRequired:
        await ky.edit(f"{ex}ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ ᴅɪ ɢʀᴜᴘ ɪɴɪ !")
 



@DANTE.UBOT("unban")
async def member_unban(client: Client, message: Message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    reply = message.reply_to_message
    zz = await eor(message, f"{prs}<b>ᴘʀᴏᴄᴇssɪɴɢ</b>...")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await zz.edit(f"<b>{ggl}ᴛɪᴅᴀᴋ ʙɪsᴀ ᴜɴʙᴀɴ ᴄʜ</b>")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await zz.edit(f"{ggl}<b>ʙᴇʀɪᴋᴀɴ ᴜsᴇʀɴᴀᴍᴇ, ᴀᴛᴀᴜ ʀᴇᴘʟʏ ᴘᴇsᴀɴɴʏᴀ</b>.")
    try:
        await message.chat.unban_member(user)
        await asyncio.sleep(0.1)
        await zz.delete()
        umention = (await client.get_users(user)).mention
        await zz.edit(f"{sks}<b>ʙᴇʀʜᴀsɪʟ ᴜɴʙᴀɴ</b> {umention}")
    except ChatAdminRequired:
        await zz.edit(f"{ggl}**ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ ᴅɪ ɢʀᴏᴜᴘ ɪɴɪ !**")
       
@DANTE.UBOT("pin|unpin")
async def pin_message(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    if not message.reply_to_message:
        return await message.edit(f"{ggl}<b>ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ ᴜɴᴛᴜᴋ ᴘɪɴ/ᴜɴᴘɪɴ</b>.")
    r = message.reply_to_message
    await message.edit(f"{prs}<b>ᴘʀᴏᴄᴇssɪɴɢ</b>...")
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.edit(
            f"{sks}<b>ᴜɴᴘɪɴɴᴇᴅ</b> [this]({r.link}) <b>ᴍᴇssᴀɢᴇ.</b>",
            disable_web_page_preview=True,
        )
    try:
        await r.pin(disable_notification=True)
        await message.edit(
            f"{sks}<b>ᴘɪɴɴᴇᴅ</b> [this]({r.link}) <b>ᴍᴇssᴀɢᴇ.</b>",
            disable_web_page_preview=True,
        )
    except ChatAdminRequired:
        await message.edit(f"{ggl}**ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ ᴅɪ ɢʀᴏᴜᴘ ɪɴɪ !**")
        await message.delete()

@DANTE.UBOT("mute|dmute")
async def mute(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id, reason = await extract_user_and_reason(message)
    nay = await eor(message, f"{prs}<b>ᴘʀᴏᴄᴇssɪɴɢ</b>...")
    if not user_id:
        return await nay.edit(f"{ggl}<b>ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
    if user_id == client.me.id:
        return await nay.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴜᴛᴇ ᴅɪʀɪ sᴇɴᴅɪʀɪ</b>")
    if user_id == OWNER_ID:
        return await nay.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴜᴛᴇ ᴅᴇᴠ</b>")
    if user_id in (await list_admins(message)):
        return await nay.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴜᴛᴇ ᴀᴅᴍɪɴ.</b>")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
{sks}<b>ᴍᴜᴛᴇᴅ ᴜsᴇʀ:</b> {mention}
{ttl}<b>ᴍᴜᴛᴇᴅ ʙʏ:</b> {message.from_user.mention if message.from_user else 'anon'}
"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()  
    if reason:
        msg += f"{ttl}<b>ᴀʟᴀsᴀɴ:</b> {reason}"
    try:
        await message.chat.restrict_member(user_id, permissions=ChatPermissions())
        await nay.edit(msg)
    except ChatAdminRequired:
        await nay.edit(f"{ggl}**ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ ᴅɪ ɢʀᴏᴜᴘ ɪɴɪ !**")
        
       
        
@DANTE.UBOT("unmute")
async def unmute(client: Client, message: Message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id = await extract_user(message)
    kl = await eor(message, f"{prs}<b>ᴘʀᴏᴄᴄᴇsɪɴɢ</b>...")
    if not user_id:
        return await kl.edit(f"{ggl}<b>ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
    try:
        await message.chat.restrict_member(user_id, permissions=unmute_permissions)
        umention = (await client.get_users(user_id)).mention
        await kl.edit(f"{sks}ʙᴇʀʜᴀsɪʟ ᴍᴇᴍʙᴜᴋᴀ ᴍᴜᴛᴇ : {umention}")        
        await kl.edit(kl)
        await kl.delete()
    except ChatAdminRequired:
        await kl.edit(f"{ggl}<b>ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ ᴅɪ ɢʀᴏᴜᴘ ɪɴɪ !</b>")
        
       


@DANTE.UBOT("kick|dkick")
async def kick_user(client: Client, message: Message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id, reason = await extract_user_and_reason(message)
    ny = await eor(message, f"{prs}<b>ᴘʀᴏᴄᴇssɪɴɢ</b>...")
    if not user_id:
        return await ny.edit(f"{ggl}<b>ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ.</b>")
    if user_id == client.me.id:
        return await ny.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ʙɪsᴀ ᴋɪᴄᴋ ᴅɪʀɪ sᴇɴᴅɪʀɪ.</b>")
    if user_id == OWNER_ID:
        return await ny.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ʙɪsᴀ ᴋɪᴄᴋ ᴅᴇᴠ!.</b>")
    if user_id in (await list_admins(message)):
        return await ny.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ʙɪsᴀ ᴋɪᴄᴋ ᴀᴅᴍɪɴ.</b>")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
{sks}<b>ᴋɪᴄᴋᴇᴅ ᴜsᴇʀ</b>: {mention}
{ttl}<b>ᴋɪᴄᴋᴇᴅ ʙʏ</b>: {message.from_user.mention if message.from_user else 'anon'}
"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"{ttl}<b>ᴀʟᴀsᴀɴ:</b> `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await ny.edit(msg)
        await ny.delete()
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        await ny.edit(f"{ggl}**ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ ᴅɪ ɢʀᴏᴜᴘ ɪɴɪ !**")
        

@DANTE.UBOT("promote")
async def promotte(client: Client, message: Message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id = await extract_user(message)
    biji = await eor(message, f"{prs}<b>ᴘʀᴏᴄᴇssɪɴɢ</b>...")
    if not user_id:
        return await biji.edit(f"{ggl}<b>ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ.</b>")
    (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    try:
        if message.command[0][0] == "f":
            await message.chat.promote_member(
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                ),
            )
            await asyncio.sleep(1)
            umention = (await client.get_users(user_id)).mention
            return await biji.edit(f"{sks}<b>ғᴜʟʟʏ ᴘʀᴏᴍᴏᴛᴇᴅ </b>: {umention}")

        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False,
            ),
        )
        await asyncio.sleep(1)
        umention = (await client.get_users(user_id)).mention
        await biji.edit(f"{sks}<b>ᴘʀᴏᴍᴏᴛᴇᴅ </b>: {umention}")
        await biji.edit(biji)
        await biji.delete()
    except ChatAdminRequired:
        await biji.edit(f"{ggl}**ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ ᴅɪ ɢʀᴏᴜᴘ ɪɴɪ !**")
      
 
@DANTE.UBOT("demote")
async def demote(client: Client, message: Message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    user_id = await extract_user(message)
    sempak = await eor(message, f"{prs}<b>ᴘʀᴏᴄᴇssɪɴɢ</b>...")
    if not user_id:
        return await sempak.edit(f"{ggl}<b>ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>")
    if user_id == client.me.id:
        return await sempak.edit(f"{ggl}<b>ᴛɪᴅᴀᴋ ʙɪsᴀ ᴅᴇᴍᴏᴛᴇ ᴅɪʀɪ sᴇɴᴅɪʀɪ.</b>")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    await asyncio.sleep(1)
    umention = (await client.get_users(user_id)).mention
    await sempak.edit(f"{sks}<b>ᴅᴇᴍᴏᴛᴇᴅ</b> : {umention}")
    await sempak.edit(sempak)
    await sempak.delete()

@DANTE.UBOT("getlink")
async def get_link(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ttl = await EMO.JUDUL(client)
    try:
        link = await client.export_chat_invite_link(message.chat.id)
        await message.reply_text(f"{sks}<b>ɪɴɪ ʜᴀsɪʟɴʏᴀ ᴛᴜᴀɴ </b>: {link}", disable_web_page_preview=True)
    except Exception as r:
        await message.reply_text(f"{ggl}<b>ᴛᴇʀᴊᴀᴅɪ ᴇʀʀᴏʀ</b> : \n {r}")
