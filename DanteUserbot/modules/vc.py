__MODULE__ = "ᴠᴄᴛᴏᴏʟs"
__HELP__ = """
**--ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴠᴄᴛᴏᴏʟꜱ--**
<blockquote><b>
• Perintah: <code>{0}startvc</code>
• Penjelasan: Untuk memulai voice chat grup.

• Perintah: <code>{0}stopvc</code>
• Penjelasan: Untuk mengakhiri voice chat grup.

• Perintah: <code>{0}jvc</code>
• Penjelasan: Untuk bergabunf voice chat grup.

• Perintah: <code>{0}lvc</code>
• Penjelasan: Untuk meninggalkan voice chat grup.

• Perintah: <code>{0}title</code>
• Penjelasan: <b>.title text</b> untuk mengubah judul obrolan suara.

• Perintah: <code>{0}listvc</code>
• Penjelasan: melihat daftar obrolan suara ada siapa saja.

</b></blockquote>
"""


from asyncio import sleep
from pytgcalls import PyTgCalls
from contextlib import suppress
from random import randint
from typing import Optional

from pyrogram import Client, enums
from pytgcalls.types import MediaStream
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall, EditGroupCallTitle
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message
from pytgcalls.exceptions import *
from pytgcalls.types.calls import Call
from DanteUserbot import *

async def get_group_call(

    client: Client, message: Message, err_msg: str = ""

) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await eor(message, f"<emoji id =5929358014627713883>❌</emoji> **No group call Found** {err_msg}")
    return False
voice_chat_participants = {}
MAX_PARTICIPANTS = 100

async def add_participant(client, chat_id):
    try:
        user = await client.get_me()
        chat = await client.get_chat(chat_id)
        
        if chat_id not in voice_chat_participants:
            voice_chat_participants[chat_id] = {}

        if user.id not in voice_chat_participants[chat_id]:
            user_data = f"[{user.first_name}](tg://user?id={user.id})"
            chat_title = chat.title
            voice_chat_participants[chat_id][user.id] = {"user": user_data, "chat": chat_title}
    except Exception as e:
        logger.error(f"Error in add_participant: {e}")

def remove_participant(chat_id, user_id):
    if chat_id in voice_chat_participants and user_id in voice_chat_participants[chat_id]:
        voice_chat_participants[chat_id].pop(user_id, None)

def get_participants_list(chat_id):
    if chat_id not in voice_chat_participants or not voice_chat_participants[chat_id]:
        return "Tidak ada pengguna dalam obrolan suara saat ini."

    participants = "\n".join(
        f"• {data['user']} di grup <code>{data['chat']}</code>"
        for data in voice_chat_participants[chat_id].values()
    )
    total_participants = len(voice_chat_participants[chat_id])
    return f"{participants}\n\n<b>Total pengguna:</b> {total_participants}"


@DANTE.UBOT("startvc")
async def opengc(client: Client, message: Message):
    bee = await eor(message, "`Processing....`")
    vctitle = get_arg(message)
    if message.chat.type == "channel":
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    args = f"<b>Active Voice Chat</b>\n • <b>Chat</b> : {message.chat.title}"
    try:
        if not vctitle:
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                )
            )
        else:
            args += f"\n • <b>Title:</b> {vctitle}"
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                    title=vctitle,
                )
            )
        await bee.edit(args)
    except Exception as e:
        await bee.edit(f"<b>INFO:</b> `{e}`")

@DANTE.UBOT("stopvc")
async def end_vc_(client: Client, message: Message):
    bee = await eor(message, f"<emoji id=6010111371251815589>⏳</emoji> `Processing....`")
    if not (group_call := await get_group_call(client, message, err_msg=", Error...")):
        return
    await client.invoke(DiscardGroupCall(call=group_call))
    await bee.edit(f"<b>Voice Chat Ended</b>\n • <b>Chat</b> : {message.chat.title}")

@DANTE.UBOT("jvc")
async def joinvc(client, message):
    bee = await eor(message, "<code>Processing....</code>")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    chat_id = int(chat_id)
    calls = await client.call_py.calls
    chat_call = calls.get(chat_id)
    if chat_call == None:
        try:
            await client.call_py.play(chat_id)
        except Exception as e:
            return await bee.edit(f"ERROR: {e}")
        await bee.edit(
            f"❏ <b>Berhasil Join Voice Chat</b>\n└ <b>Chat :</b><code>{message.chat.title}</code>"
        )
        await sleep(1)
        await bee.delete()
    else:
        return await bee.edit("<b>Akun Kamu Sudah Berada Di Atas</b>")

@DANTE.UBOT("lvc")
async def leavevc(client, message):
    bee = await eor(message, "<code>Processing....</code>")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    chat_id = int(chat_id)
    calls = await client.call_py.calls
    chat_call = calls.get(chat_id)
    if chat_call == None:
        return await bee.edit("<b>Kamu Belum Bergabung Ke Voice Chat</b>")
    else:
        try:
            await client.call_py.leave_call(chat_id)
            await bee.edit(f"**❏ Berhasil Meninggalkan Voice Chat <emoji id=5798623990436074786>✅</emoji>**\n")
            await sleep(1)
            await bee.delete()
        except Exception as e:
            return await message.reply_text(e)

@DANTE.UBOT("title")
async def vctittle(client, message):
    txt = client.get_arg(message)
    ky = await message.reply("proses")
    if len(message.command) < 2:
        await ky.edit("gagal mengubah judul obrolan suara")
        return
    if not (group_call := (await get_group_call(client, message, err_msg=", Kesalahan..."))):
        return
    try:
        await client.invoke(EditGroupCallTitle(call=group_call, title=f"{txt}"))

    except Forbidden:
        await ky.edit("seperti ada kesalahan")
        return
    await ky.edit("berhasil mengubah judul obralan suara")
    return

@DANTE.UBOT("listvc")
async def list_vc(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title if hasattr(message.chat, 'title') else 'Obrolan'
    voice_chat_list = get_participants_list(chat_id)
    
    if chat_id not in voice_chat_participants or not voice_chat_participants[chat_id]:
        await message.reply("<b>Tidak ada pengguna dalam obrolan suara saat ini.</b>")
        return

    participants = "\n".join(
        f"• {data['user']} di grup <code>{data['chat']}</code>"
        for data in voice_chat_participants[chat_id].values()
    )
    total_participants = len(voice_chat_participants[chat_id])
    interactive_list = f"<b>Daftar Pengguna dalam Obrolan Suara:</b>\n\n{participants}\n\n<b>Total pengguna:</b> {total_participants}"

    await message.reply(interactive_list)


@DANTE.DEVS("Jvcu")
async def jvcs(client, message):
    ky = await message.reply("proses")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if "/+" in str(chat_id):
        gid = await client.get_chat(str(chat_id))
        chat_id = int(gid.id)
    elif "t.me/" in str(chat_id) or "@" in str(chat_id):
        chat_id = chat_id.replace("https://t.me/", "")
        gid = await client.get_chat(str(chat_id))
        chat_id = int(gid.id)
    else:
        chat_id = int(chat_id)
    try:
        chat = await client.get_chat(chat_id)
        title = chat.title
    except:
        title = "Private"
    if chat_id:
        try:
            await client.call_py.play(chat_id)
            await client.call_py.mute_stream(chat_id)
            await message.reply("berhasil naik ke obrolan suara")

        except NoActiveGroupCall:
            await message.reply(
                f"<b>Tidak ada Obrolan suara aktif di <code>{title}</code></b>"
            )
        except AlreadyJoinedError:
            await message.reply(f"<b>Akun anda sudah berada di Obrolan Suara.</b>")
        except GroupCallNotFound:
            await client.call_py.play(chat_id)
            await client.call_py.mute_stream(chat_id)
            await message.reply("berhasil naik ke obrolan suara")

        except Exception as e:
            await message.reply("err")
        return await ky.delete()
    else:
        return


@DANTE.DEVS("lvcu")
async def lvcs(client, message):
    ky = await message.reply("proses")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if "/+" in str(chat_id):
        gid = await client.get_chat(str(chat_id))
        chat_id = int(gid.id)
    elif "t.me/" in str(chat_id) or "@" in str(chat_id):
        chat_id = chat_id.replace("https://t.me/", "")
        gid = await client.get_chat(str(chat_id))
        chat_id = int(gid.id)
    else:
        chat_id = int(chat_id)
    try:
        chat = await client.get_chat(chat_id)
        title = chat.title
    except:
        title = "Private"
    if chat_id:
        try:
            await client.call_py.leave_call(chat_id)
            await ky.edit("berhasil turun dari obrolan suara")
            return
        except NotInCallError:
            return await ky.edit(
                f"<b>Anda sedang tidak berada di Obrolan Suara <code>{title}</code></b>"
            )
        except Exception as e:
            await ky.edit("err")
            return
    else:
        return

