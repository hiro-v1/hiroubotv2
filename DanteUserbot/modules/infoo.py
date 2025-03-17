from asyncio import gather
from os import remove

from pyrogram.enums import ChatType

from DanteUserbot import *

__MODULE__ = "ɪɴғᴏ"
__HELP__ = f"""<blockquote><b>
<b>『 bantuan untuk info 』</b>

  <b>• perintah:</b> <code>{PREFIX[0]}info</code> [user_id/username/reply to users]
  <b>• penjelasan:</b> untuk mendapatkan info pengguna telegram dengan deskripsi lengkap

  <b>• perintah:</b> <code>{PREFIX[0]}cinfo</code> [chat_id/username/reply to chat]
  <b>• penjelasan:</b> untuk mendapatkan info group/channel dengan deskripsi lengkap
</b></blockquote>"""


@DANTE.UBOT("info")
async def info_cmd(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply("</b><emoji id=6010111371251815589>⏳</emoji> processing . . .</b>")
    if not user_id:
        return await Tm.edit(
            f"<emoji id =5375452661036358740>🔥</emoji> **berikan userid/username/reply untuk mendapatkan info pengguna tersebut **"
        )
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""
<b>user information:</b>

🆔 <b>user id:</b> <code>{user.id}</code>
👤 <b>first name:</b> {first_name}
🗣️ <b>last name:</b> {last_name}
🌐 <b>username:</b> {username}
🏛️ <b>dc id:</b> <code>{dc_id}</code>
🤖 <b>is bot:</b> <code>{user.is_bot}</code>
🚷 <b>is scam:</b> <code>{user.is_scam}</code>
🚫 <b>restricted:</b> <code>{user.is_restricted}</code>
✅ <b>verified:</b> <code>{user.is_verified}</code>
⭐ <b>premium:</b> <code>{user.is_premium}</code>
📝 <b>user bio:</b> {bio}

👀 <b>same groups seen:</b> {len(common)}
👁️ <b>last seen:</b> <code>{status}</code>
🔗 <b>user permanent link:</b> <a href=tg://user?id={user.id}>{fullname}</a>
"""
        photo_id = user.photo.big_file_id if user.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Tm.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=message.id,
                ),
            )
            remove(photo)
        else:
            await Tm.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(f"info: {e}")

@DANTE.UBOT("cinfo")
async def cinfo_cmd(client, message):
    Tm = await message.reply("</b><emoji id=6010111371251815589>⏳</emoji> processing . . .</b>")
    try:
        if len(message.text.split()) > 1:
            chat_u = message.text.split()[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await Tm.edit(
                    f"<emoji id =5929358014627713883>❌</emoji> gunakan perintah ini di dalam grup atau gunakan {PREFIX[0]}cinfo [group username atau id]"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Private"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""
<b>chat information:</b>

🆔 <b>chat id:</b> <code>{chat.id}</code>
👥 <b>title:</b> {chat.title}
👥 <b>username:</b> {username}
📩 <b>type:</b> <code>{type}</code>
🏛️ <b>dc id:</b> <code>{dc_id}</code>
🗣️ <b>is scam:</b> <code>{chat.is_scam}</code>
🎭 <b>is fake:</b> <code>{chat.is_fake}</code>
✅ <b>verified:</b> <code>{chat.is_verified}</code>
🚫 <b>restricted:</b> <code>{chat.is_restricted}</code>
🔰 <b>protected:</b> <code>{chat.has_protected_content}</code>

🚻 <b>total members:</b> <code>{chat.members_count}</code>
📝 <b>description:</b> <code>{description}</code>
"""
        photo_id = chat.photo.big_file_id if chat.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Tm.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=message.id,
                ),
            )
            remove(photo)
        else:
            await Tm.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(f"info: `{e}`")
