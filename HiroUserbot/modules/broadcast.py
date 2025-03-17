import asyncio
import random

from gc import get_objects
from asyncio import sleep
from pyrogram.raw.functions.messages import DeleteHistory, StartBot
from pyrogram.enums import ChatType
from pyrogram import *
from pyrogram.types import *
from pyrogram.errors.exceptions import FloodWait
from HiroUserbot import *

__MODULE__ = "ɢᴄᴀsᴛ"
__HELP__ = """
**--Bantuan untuk Broadcast--**
<blockquote><b>
<b>command:</b> <code>{0}gcast</code>
<b>command:</b> <code>{0}gcast mulai broadcast digroup</code>
<b>command:</b> <code>{0}bcfd</code> <b>or</b> <code>{0}cfd</code>

<b>mengirim pesan siaran secara forward</b>
<b>command:</b> <code>{0}send</code>
<b>mengirim pesan ke user/group/channel</b>

<b>spesial</b>
<b>command:</b> <code>{0}ucast users</code>
<b>command:</b> <code>Untuk mengirim pesan siaran ke users contoh: ucast users hai</code>
<b>command:</b> <code>{0}gikes all</code>
<b>mengirim pesan ke user/group/channels contoh gikes all hallo</b>
<b>command stop:</b> <code>{0}stopg agar memberhentikan ucast/gikes.</code>

<b>command:</b> <code>{0}bcast</code>
<b>example:</b> <code>bcast untuk grup</code> <code>bcast gcast yang bisa di cancel</code>
<b>command:</b> <code>{0}gcan</code>
<b>example:</b> <code>untuk memberhentikan bcast</code> <code>bcast gcast yang bisa di cancel</code>

<b>command:</b> <code>{0}autogikes</code>
<b>mengirim pesan siaran secara otomatis</b>
<b>query:</b>
<code>|on/off |text |delay |remove |limit</code></b></blockquote>
"""


def get_message(message):
    msg = (
        message.reply_to_message
        if message.reply_to_message
        else ""
        if len(message.command) < 2
        else " ".join(message.command[1:])
    )
    return msg
  
async def get_data_id(client, query):
    chat_types = {
        "global": [ChatType.CHANNEL, ChatType.GROUP, ChatType.SUPERGROUP],
        "all": [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE],
        "group": [ChatType.GROUP, ChatType.SUPERGROUP],
        "users": [ChatType.PRIVATE],
    }
    return [dialog.chat.id async for dialog in client.get_dialogs() if dialog.chat.type in chat_types.get(query, [])]

async def add_auto_text(client, text):
    auto_text = await get_vars(client.me.id, "AUTO_TEXT") or []
    auto_text.append(text)
    await set_vars(client.me.id, "AUTO_TEXT", auto_text)

def extract_type_and_msg(message):
    args = message.text.split(None, 2)
    if len(args) < 2:
        return None, None
    
    type = args[1]
    msg = message.reply_to_message if message.reply_to_message else args[2] if len(args) > 2 else None
    return type, msg

def extract_type_and_text(message):
    args = message.text.split(None, 2)
    if len(args) < 2:
        return None, None

    type = args[1]
    msg = (
        message.reply_to_message.text
        if message.reply_to_message
        else args[2]
        if len(args) > 2
        else None
    )
    return type, msg

async def limit_cmd(client, message):
    prs = await EMO.PROSES(client)
    await client.unblock_user("SpamBot")
    bot_info = await client.resolve_peer("SpamBot")
    _msg = f"{prs}proceꜱꜱing...</b>"

    msg = await message.reply(_msg)
    response = await client.invoke(
        StartBot(
            bot=bot_info,
            peer=bot_info,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await sleep(1)
    await msg.delete()
    status = await client.get_messages("SpamBot", response.updates[1].message.id + 1)
    await status.copy(message.chat.id, reply_to_message_id=message.id)
    return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))


broadcast_running = False

@HIRO.UBOT("bcast")
async def broadcast_group_cmd(client, message):
    global broadcast_running

    msg = await message.reply("Processing...", quote=True)

    send = get_message(message)
    if not send:
        return await msg.edit("Silakan balas ke pesan atau berikan pesan.")

    broadcast_running = True

    chats = await get_data_id(client, "group")
    blacklist = await get_chat(client.me.id)

    done = 0
    failed = 0
    
    for chat_id in chats:

        if not broadcast_running:
            break
        
        if chat_id not in blacklist and chat_id not in BLACKLIST_CHAT:
            
            try:
                if message.reply_to_message:
                    await send.copy(chat_id)
                else:
                    await client.send_message(chat_id, send)
                done += 1
                await asyncio.sleep(0.1)
            except Exception:
                failed += 1
                pass
                await asyncio.sleep(1)
                                
    broadcast_running = True

    if done > 0:
        await msg.edit(f"**<emoji id=5780777456428388142>🤖</emoji>Berhasil Terkirim:** `{done}` \n**<emoji id=5019523782004441717>❌</emoji>Gagal Mengirim Pesan Ke:** `{failed}`.")
    else:
        await msg.edit(f"**Pesan Broadcast Berhasil Dibatalkan**.")

@HIRO.UBOT("gcan")
async def cancel_broadcast(client, message):
    global broadcast_running

    if not broadcast_running:
        return await eor(message, "<code>Tidak ada pengiriman pesan global yang sedang berlangsung.</code>")

    broadcast_running = False
    await eor(message, "<b>Pengiriman pesan global telah dibatalkan!</b>")



@HIRO.UBOT("gcast")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)
    _msg = f"<b>{prs}proccesing...</b>"
    gcs = await message.reply(_msg)
    if not message.reply_to_message:
        return await gcs.edit(f"**{ggl} mohon balas ke pesan !**")
    text = message.reply_to_message
    chats = await get_data_id(client, "group")
    blacklist = await get_list_from_vars(client.me.id, "BL_ID")
    done = 0
    failed = 0
    for chat_id in chats:
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue

        try:
            await text.copy(chat_id)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await text.copy(chat_id)
            done += 1
        except Exception:
            failed += 1
            pass
    if client.me.is_premium:
        await gcs.delete()
        _gcs = f"""
{bcs}<emoji id=6037164425356514018>😘</emoji><emoji id=6037583326401794925>😘</emoji><emoji id=6037242439142481737>😘</emoji><emoji id=6037315105694160163>😘</emoji><emoji id=6037431009681609488>😘</emoji><emoji id=6037252029804450164>😘</emoji><emoji id=6034895892350245694>😘</emoji><emoji id=6037220122492408602>😘</emoji><emoji id=6037164425356514018>😘</emoji>

<b>{brhsl} berrhasil kirim ke {done} group</b>
<b>{ggl} gagal kirim ke {failed} group</b>

"""
    else:
        await gcs.delete()
        _gcs = f"""
<b>gcast telah selesai</b>
<b>berrhasil {done} group</b>
<b>gagal {failed} group</b>
"""
    return await message.reply(_gcs)


@HIRO.UBOT("bcfd|cfd")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)
    
    _msg = f"<b>{prs}proceꜱꜱing...</b>"
    gcs = await message.reply(_msg)

    command, text = extract_type_and_msg(message)
    
    if command not in ["group", "users", "all"] or not text:
        return await gcs.edit(f"{ggl}<code>{message.text.split()[0]}</code> <b>type [reply]</b>")

    if not message.reply_to_message:
        return await gcs.edit(f"{ggl}<code>{message.text.split()[0]}</code> <b>type [reply]</b>")

    chats = await get_data_id(client, command)
    blacklist = await get_list_from_vars(client.me.id, "BL_ID")

    done = 0
    failed = 0
    for chat_id in chats:
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue

        try:
            if message.reply_to_message:
                await message.reply_to_message.forward(chat_id)
            else:
                await text.forward(chat_id)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if message.reply_to_message:
                await message.reply_to_message.forward(chat_id)
            else:
                await text.forward(chat_id)
            done += 1
        except Exception:
            failed += 1
            pass

    await gcs.delete()
    _gcs = f"""
<b>{bcs}broadcaꜱt fordward done</b>
<b>{brhsl}ꜱucceꜱ {done} group</b>
<b>{ggl}failed {failed} group</b>
"""
    return await message.reply(_gcs)

@HIRO.UBOT("addbl")
@HIRO.GROUP
async def _(client, message):
    prs = await EMO.PROSES(client)
    grp = await EMO.BL_GROUP(client)
    _msg = f"<b>{prs}proceꜱꜱing...</b>"

    msg = await message.reply(_msg)
    try:
        chat_id = message.chat.id
        blacklist = await get_list_from_vars(client.me.id, "BL_ID")

        if chat_id in blacklist:
            txt = f"""
{grp} <b>group:</b> {message.chat.title}  <b>ꜱudah ada dalam blackliꜱt broadcaꜱt</b>
"""
        else:
            await add_to_vars(client.me.id, "BL_ID", chat_id)
            txt = f"""
{grp} <b>group:</b> {message.chat.title}  <b>berhaꜱil di tambahkan ke blackliꜱt broadcaꜱt</b>
"""

        return await msg.edit(txt)
    except Exception as error:
        return await msg.edit(str(error))


@HIRO.UBOT("unbl")
@HIRO.GROUP
async def _(client, message):
    prs = await EMO.PROSES(client)
    grp = await EMO.BL_GROUP(client)
    _msg = f"<b>{prs}proceꜱꜱing...</b>"

    msg = await message.reply(_msg)
    try:
        chat_id = get_arg(message) or message.chat.id
        blacklist = await get_list_from_vars(client.me.id, "BL_ID")

        if chat_id not in blacklist:
            response = f"""
{grp} <b>group:</b> {message.chat.title}  <b>tidak ada dalam blackliꜱt broadcaꜱt</b>
"""
        else:
            await remove_from_vars(client.me.id, "BL_ID", chat_id)
            response = f"""
{grp} <b>group:</b> {message.chat.title}  <b>berhaꜱil di hapuꜱ dalam blackliꜱt broadcaꜱt</b>
"""

        return await msg.edit(response)
    except Exception as error:
        return await msg.edit(str(error))


@HIRO.UBOT("listbl")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ktrng = await EMO.BL_KETERANGAN(client)
    _msg = f"<b>{prs}proceꜱꜱing...</b>"
    mzg = await message.reply(_msg)

    blacklist = await get_list_from_vars(client.me.id, "BL_ID")
    total_blacklist = len(blacklist)

    list = f"{brhsl} daftar blackliꜱt\n"

    for chat_id in blacklist:
        try:
            chat = await client.get_chat(chat_id)
            list += f" ├ {chat.title} | {chat.id}\n"
        except:
            list += f" ├ {chat_id}\n"

    list += f"{ktrng} total blackliꜱt {total_blacklist}"
    return await mzg.edit(list)


@HIRO.UBOT("rallbl")
async def _(client, message):
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    brhsl = await EMO.BERHASIL(client)
    _msg = f"<b>{prs}proceꜱꜱing...</b>"

    msg = await message.reply(_msg)
    blacklists = await get_list_from_vars(client.me.id, "BL_ID")

    if not blacklists:
        return await msg.edit(f"<b>{ggl}blackliꜱt broadcaꜱt anda koꜱong</b>")

    for chat_id in blacklists:
        await remove_from_vars(client.me.id, "BL_ID", chat_id)

    await msg.edit(f"<b>{brhsl}ꜱemua blackliꜱt broadcaꜱt berhaꜱil di hapuꜱ</b>")


AG = []
LT = []


@HIRO.UBOT("autogikes")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    bcs = await EMO.BROADCAST(client)
    mng = await EMO.MENUNGGU(client)
    ggl = await EMO.GAGAL(client)   
    msg = await message.reply(f"<b>{prs}proceꜱꜱing...</b>")
    type, value = extract_type_and_text(message)
    auto_text_vars = await get_vars(client.me.id, "AUTO_TEXT")

    if type == "on":
        if not auto_text_vars:
            return await msg.edit(
                f"<b>{ggl}harap ꜱetting text terlebih dahulu</b>"
            )

        if client.me.id not in AG:
            await msg.edit(f"<b>{brhsl}auto gcaꜱt di aktifkan</b>")

            AG.append(client.me.id)

            done = 0
            while client.me.id in AG:
                delay = await get_vars(client.me.id, "DELAY_GCAST") or 1
                blacklist = await get_list_from_vars(client.me.id, "BL_ID")
                txt = random.choice(auto_text_vars)

                group = 0
                async for dialog in client.get_dialogs():
                    if (
                        dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)
                        and dialog.chat.id not in blacklist
                    ):
                        try:
                            await asyncio.sleep(1)
                            await client.send_message(dialog.chat.id, f"{txt} {random.choice(range(999))}")
                            group += 1
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            await client.send_message(dialog.chat.id, f"{txt} {random.choice(range(999))}")
                            group += 1
                        except Exception:
                            pass

                if client.me.id not in AG:
                    return

                done += 1
                await msg.reply(f"""
<b>{bcs}auto_gcaꜱt done</b>
<b>putaran</b> {done}
<b>{brhsl}ꜱucceꜱ</b> {group} <b>group</b>
<b>{mng}wait</b> {delay} <b>minuteꜱ</b>
""",
                    quote=True,
                )
                await asyncio.sleep(int(60 * int(delay)))
        else:
            return await msg.delete()

    elif type == "off":
        if client.me.id in AG:
            AG.remove(client.me.id)
            return await msg.edit(f"<b>{brhsl}auto gcast dinonaktifkan</b>")
        else:
            return await msg.delete()

    elif type == "text":
        if not value:
            return await msg.edit(
                f"<b>{ggl}<code>{message.text.split()[0]} text</code> - [value]</b>"
            )
        await add_auto_text(client, value)
        return await msg.edit(f"<b>{brhsl}berhasil di simpan</b>")

    elif type == "delay":
        if not int(value):
            return await msg.edit(
                f"<b>{ggl}<code>{message.text.split()[0]} delay</code> - [value]</b>"
            )
        await set_vars(client.me.id, "DELAY_GCAST", value)
        return await msg.edit(
            f"<b>{brhsl}barhasil ke setting {value} menit</b>"
        )

    elif type == "remove":
        if not value:
            return await msg.edit(
                f"<b>{ggl}<code>{message.text.split()[0]} remove</code> - [value]</b>"
            )
        if value == "all":
            await set_vars(client.me.id, "AUTO_TEXT", [])
            return await msg.edit(f"<b>{brhsl}semua text berhasil dihapus</b>")
        try:
            value = int(value) - 1
            auto_text_vars.pop(value)
            await set_vars(client.me.id, "AUTO_TEXT", auto_text_vars)
            return await msg.edit(
                f"<b>{brhsl}text ke {value+1} berhasil dihapus</b>"
            )
        except Exception as error:
            return await msg.edit(str(error))

    elif type == "list":
        if not auto_text_vars:
            return await msg.edit(f"<b>{ggl}auto gcast text kosong</b>")
        txt = "<b>daftar auto gcast text</b>\n\n"
        for num, x in enumerate(auto_text_vars, 1):
            txt += f"<b>{num}⊯></b> {x}\n\n"
        txt += f"<b>\nuntuk menghapus text:\n<code>{message.text.split()[0]} remove</code> [angka/all]</b>"
        return await msg.edit(txt)

    elif type == "limit":
        if value == "off":
            if client.me.id in LT:
                LT.remove(client.me.id)
                return await msg.edit(f"<b>{brhsl}auto cek limit dinonaktifkan</b>")
            else:
                return await msg.delete()

        elif value == "on":
            if client.me.id not in LT:
                LT.append(client.me.id)
                await msg.edit(f"<b>{brhsl}auto cek limit started</b>")
                while client.me.id in LT:
                    for x in range(2):
                        await limit_cmd(client, message)
                        await asyncio.sleep(5)
                    await asyncio.sleep(1200)
            else:
                return await msg.delete()
        else:
             return await msg.edit(f"<b>{ggl}<code>{message.text.split()[0]} limit</code> - [value]</b>")

    else:
        return await msg.edit(f"<b>{ggl}<code>{message.text.split()[0]}</code> [query] - [value]</b>")

gcast_progress = []

@HIRO.UBOT("ucast")
async def gcast_handler(client, message):
    global gcast_progress
    gcast_progress.append(client.me.id)
    
    prs = await EMO.PROSES(client)
    sks = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)
    ktrng = await EMO.BL_KETERANGAN(client)    
    _msg = f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs...</b>"
    gcs = await message.reply(_msg)    
    command, text = extract_type_and_msg(message)

    if command not in ["users"] or not text:
        gcast_progress.remove(client.me.id)
        return await gcs.edit(f"<blockquote><code>{message.text.split()[0]}</code> <b>[ᴛʏᴘᴇ] [ᴛᴇxᴛ/ʀᴇᴘʟʏ]</b> {ggl}</blockquote>")
    chats = await get_data_id(client, command)
    blacklist = await get_list_from_vars(client.me.id, "BL_ID")

    done = 0
    failed = 0
    for chat_id in chats:
        if client.me.id not in gcast_progress:
            await gcs.edit(f"<blockquote><b>ᴘʀᴏsᴇs ɢᴄᴀsᴛ ʙᴇʀʜᴀsɪʟ ᴅɪ ʙᴀᴛᴀʟᴋᴀɴ !</b> {sks}</blockquote>")
            return
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue

        try:
            if message.reply_to_message:
                await text.copy(chat_id)
            else:
                await client.send_message(chat_id, text)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                if message.reply_to_message:
                    await text.copy(chat_id)
                else:
                    await client.send_message(chat_id, text)
                done += 1
            except (Exception, ChannelPrivate):
                failed += 1
        except (Exception, ChannelPrivate):
            failed += 1

    gcast_progress.remove(client.me.id)
    await gcs.delete()
    _gcs = f"""
<blockquote><b>{bcs}ʙʀᴏᴀᴅᴄᴀsᴛ ᴛᴇʀᴋɪʀɪᴍ</b></blockquote>
<blockquote><b>{sks}ʙᴇʀʜᴀsɪʟ : {done} ᴄʜᴀᴛ</b>
<b>{ggl}ɢᴀɢᴀʟ : {failed} ᴄʜᴀᴛ</b>
<b>{ktrng}ᴛʏᴘᴇ :</b> <code>{command}</code></blockquote>
"""
    return await message.reply(_gcs)



  
