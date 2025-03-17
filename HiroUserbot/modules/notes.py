from pyrogram.types import *

from HiroUserbot import *

async def get_pm_id(user_id):
    pm_id = await get_vars(user_id, "PM_PERMIT")
    return [int(x) for x in str(pm_id).split()] if pm_id else []


async def add_pm_id(me_id, user_id):
    pm_id = await get_vars(me_id, "PM_PERMIT")
    if pm_id:
        user_id = f"{pm_id} {user_id}"
    await set_vars(me_id, "PM_PERMIT", user_id)


async def remove_pm_id(me_id, user_id):
    pm_id = await get_vars(me_id, "PM_PERMIT")
    if pm_id:
        list_id = [int(x) for x in str(pm_id).split() if x != str(user_id)]
        await set_vars(me_id, "PM_PERMIT", " ".join(map(str, list_id)))

__MODULE__ = "ɴᴏᴛᴇs"
__HELP__ = """<blockquote><b>
Document for <b>Notes</b>

<b>command:</b> <code>{0}addnote</code> [name]
   <i>menyimpan sebuah catatan</i>

<b>command:</b> <code>{0}addcb</code> [name]
   <i>menyimpan sebuah callback</i>

<b>command:</b> <code>{0}get</code> [name]
   <i>mendapatkan catatan yang di simpan</i>
 
<b>command:</b> <code>{0}delnote</code> [name]
   <i>menghapus catatan yang di simpan</i>

<b>command:</b> <code>{0}delcb</code> [name]
   <i>menghapus callback yang di simpan</i>
 
<b>command:</b> <code>{0}listnote</code>
  <i>melihat daftar catatan yang di simpan</i>

<b>command:</b> <code>{0}listcb</code>
  <i>melihat daftar callback yang di simpan</i>

<b>for button:</b>
<b>format | nama tombol - url/callback |</code></b></blockquote>
"""


@HIRO.UBOT("addnote|addcb")
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    args = get_arg(message)
    reply = message.reply_to_message
    query = "notes_cb" if message.command[0] == "addcb" else "notes"

    if not args or not reply:
        return await message.reply(
            f"<code>{message.text.split()[0]}</code> <b>[name] [text/reply]</b>"
        )

    vars = await get_vars(client.me.id, args, query)

    if vars:
        return await message.reply(f"<b>{ggl}catatan {args} ꜱudah ada</n>")

    value = None
    type_mapping = {
        "text": reply.text,
        "photo": reply.photo,
        "voice": reply.voice,
        "audio": reply.audio,
        "video": reply.video,
        "animation": reply.animation,
        "sticker": reply.sticker,
    }

    for media_type, media in type_mapping.items():
        if media:
            send = await reply.copy(client.me.id)
            value = {
                "type": media_type,
                "message_id": send.id,
            }
            break

    if value:
        await set_vars(client.me.id, args, value, query)
        return await message.reply(
            f"<b>{brhsl}catatan <code>{args}</code> berhasil tersimpan</b>"
        )
    else:
        return await message.reply(
            f"<code>{message.text.split()[0]}</code> <b>[name] [text/reply]</b>"
        )


@HIRO.UBOT("delnote|delcb")
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    args = get_arg(message)

    if not args:
        return await message.reply(
            f"<code>{message.text.split()[0]}</code> <b>[name]</b>"
        )

    query = "notes_cb" if message.command[0] == "delcb" else "notes"
    vars = await get_vars(client.me.id, args, query)

    if not vars:
        return await message.reply(f"<b>{ggl}catatan {args} tidak ditemukan</b>")

    await remove_vars(client.me.id, args, query)
    await client.delete_messages(client.me.id, int(vars["message_id"]))
    return await message.reply(f"<brhsl>{brhsl}catan {args} berhasil dihapus</b>")


@HIRO.UBOT("get")
async def _(client, message):
    ggl = await EMO.GAGAL(client)
    msg = message.reply_to_message or message
    args = get_arg(message)

    if not args:
        return await message.reply(
            f"<code>{message.text.split()[0]}</code> <b>[name]</b>"
        )

    data = await get_vars(client.me.id, args, "notes")

    if not data:
        return await message.reply(
            f"<b>{ggl}catatan {args} tidak ditemukan</b>"
        )

    m = await client.get_messages(client.me.id, int(data["message_id"]))

    if data["type"] == "text":
        if matches := re.findall(r"\| ([^|]+) - ([^|]+) \|", m.text):
            try:
                x = await client.get_inline_bot_results(
                    bot.me.username, f"get_notes {client.me.id} {args}"
                )
                return await client.send_inline_bot_result(
                    message.chat.id,
                    x.query_id,
                    x.results[0].id,
                    reply_to_message_id=msg.id,
                )
            except Exception as error:
                await message.reply(error)
        else:
            return await m.copy(message.chat.id, reply_to_message_id=msg.id)
    else:
        return await m.copy(message.chat.id, reply_to_message_id=msg.id)


@HIRO.UBOT("listnote|listcb")
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    ktrng = await EMO.BL_KETERANGAN(client)
    query = "notes_cb" if message.command[0] == "listcb" else "notes"
    vars = await all_vars(client.me.id, query)
    if vars:
        msg = f"<b>{brhsl}daftar catatan</b>\n\n"
        for x, data in vars.items():
            msg += f" {x} |({data['type']})\n"
        msg += f"<b>\n{ktrng}total catatan: {len(vars)}</b>"
    else:
        msg = f"<b>{ggl}tidak ada catatan</b>"

    return await message.reply(msg, quote=True)


@HIRO.INLINE("^get_notes")
async def _(client, inline_query):
    query = inline_query.query.split()
    data = await get_vars(int(query[1]), query[2], "notes")
    item = [x for x in ubot._ubot if int(query[1]) == x.me.id]
    for me in item:
        m = await me.get_messages(int(me.me.id), int(data["message_id"]))
        buttons, text = create_inline_keyboard(m.text, f"{int(query[1])}_{query[2]}")
        return await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                (
                    InlineQueryResultArticle(
                        title="get notes!",
                        reply_markup=buttons,
                        input_message_content=InputTextMessageContent(text),
                    )
                )
            ],
        )


@HIRO.CALLBACK("_gtnote")
async def _(client, callback_query):
    _, user_id, *query = callback_query.data.split()
    data_key = "notes_cb" if bool(query) else "notes"
    query_eplit = query[0] if bool(query) else user_id.split("_")[1]
    data = await get_vars(int(user_id.split("_")[0]), query_eplit, data_key)
    item = [x for x in ubot._ubot if int(user_id.split("_")[0]) == x.me.id]
    for me in item:
        m = await me.get_messages(int(me.me.id), int(data["message_id"]))
        buttons, text = create_inline_keyboard(
            m.text, f"{int(user_id.split('_')[0])}_{user_id.split('_')[1]}", bool(query)
        )
        return await callback_query.edit_message_text(text, reply_markup=buttons)
